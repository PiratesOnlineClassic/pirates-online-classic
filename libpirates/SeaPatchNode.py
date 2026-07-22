import threading
from typing import List
from panda3d.core import PandaNode, NodePath, GeomNode, Geom, GeomVertexData, GeomVertexWriter, GeomVertexRewriter, LPoint3f, LVecBase3f, LVecBase2f, LPoint2f, LVecBase4f, InternalName, GeomVertexArrayFormat, GeomVertexFormat, TransformState, ClockObject, Thread


class SeaPatchNode(PandaNode):
    """
    Node for rendering sea patches with dynamic wave deformation.
    """

    def __init__(self, name: str, root):
        super().__init__(name)
        self.m_root = root
        self.m_want_z = True
        self.m_want_reflect = True
        self.m_want_color = True
        self.m_want_uv = True
        self.m_want_normal = True
        self.m_z_offset = 0.0
        self.m_last_update = 0.0
        self.m_lock = threading.Lock()
        self.m_geoms = []
        self.m_flat_geoms = []

    def setWantZ(self, want_z: bool):
        self.m_want_z = want_z

    def getWantZ(self):
        return self.m_want_z

    def setWantReflect(self, want_reflect: bool):
        self.m_want_reflect = want_reflect

    def getWantReflect(self):
        return self.m_want_reflect

    def setWantColor(self, want_color: bool):
        self.m_want_color = want_color

    def getWantColor(self):
        return self.m_want_color

    def setWantUv(self, want_uv: bool):
        self.m_want_uv = want_uv

    def getWantUv(self):
        return self.m_want_uv

    def setWantNormal(self, want_normal: bool):
        self.m_want_normal = want_normal

    def getWantNormal(self):
        return self.m_want_normal

    def setZOffset(self, offset: float):
        self.m_z_offset = offset

    def getZOffset(self):
        return self.m_z_offset

    def calcReflection(self, normal: LVecBase3f, d: LPoint3f, result: LVecBase3f):
        dot_product = normal.dot(d)
        scaled_normal = normal * 2 * dot_product
        reflected_vector = d - scaled_normal
        reflected_vector.normalize()
        result[0] = reflected_vector[0]
        result[1] = reflected_vector[1]
        result[2] = reflected_vector[2]

    def hasCullCallback(self):
        return True

    def safeToTransform(self):
        return False

    def cullCallback(self, trav, data):
        # NOTE: Panda3D's C++ CullTraverser only ever calls this if
        # PandaNode.set_cull_callback() was called in the node's
        # constructor (it sets an internal "fancy bits" flag checked on
        # every node during cull). That method is protected/unpublished in
        # Panda3D's Python bindings, so a pure-Python PandaNode subclass
        # like this one has no way to call it - this method is therefore
        # NEVER actually invoked by the engine. It's kept here for parity
        # with the original C++ implementation this was ported from. The
        # real per-frame update path is update(), which performs the same
        # computation but is driven by a regular Python task instead (see
        # SeaPatch.camTask).
        with self.m_lock:
            if not (self.m_root and self.m_root.isEnabled()):
                return True

            if not self._shouldUpdate():
                return True

            np = trav.get_scene().get_cull_center()
            if np.is_empty():
                np = trav.get_scene().get_camera_path()

            if np.is_empty():
                return False

            current_thread = trav.get_current_thread()
            node_path = data.get_node_path()
            self._updateGeoms(node_path, np, current_thread)
            return True

    def update(self, node_path: NodePath):
        """
        Recomputes wave-deformed vertex positions/normals/UVs for this
        frame. This is the real update path used at runtime (see the note
        in cullCallback() for why the normal Panda3D cull-callback
        mechanism can't be used from a pure-Python PandaNode subclass).
        Call this once per frame (e.g. from a task), after `node_path`
        (the NodePath wrapping this SeaPatchNode) has been positioned for
        the current frame.
        """
        with self.m_lock:
            if not (self.m_root and self.m_root.isEnabled()):
                return

            if not self._shouldUpdate():
                return

            current_thread = Thread.get_current_thread()
            np = self.m_root.getCenter()
            if np.is_empty():
                np = node_path

            self._updateGeoms(node_path, np, current_thread)

    def _shouldUpdate(self):
        time = ClockObject.get_global_clock().get_frame_time()
        if time == self.m_last_update:
            return False

        self.m_last_update = time
        return True

    def _updateGeoms(self, node_path: NodePath, np: NodePath, current_thread):
        transform = node_path.get_net_transform(current_thread)

        anchor_trans = self.m_root.getAnchor().get_net_transform(current_thread)
        anchor_trans = anchor_trans.invert_compose(transform)
        anchor_mat = anchor_trans.get_mat()

        center_trans = self.m_root.getCenter().get_net_transform(current_thread)
        center_trans = center_trans.invert_compose(transform)
        center_mat = center_trans.get_mat()

        anchor_rel_trans = self.m_root.getAnchor().get_transform(np, current_thread)
        anchor_rel_mat = anchor_rel_trans.get_mat()

        for geom in self.m_flat_geoms:
            self.doFlat(geom, anchor_mat, center_mat, anchor_rel_mat, current_thread)

        for geom in self.m_geoms:
            self.doWave(geom, anchor_mat, center_mat, anchor_rel_mat, current_thread)

    def collectGeometry(self):
        self.m_geoms.clear()
        self.m_flat_geoms.clear()
        self.rCollectGeometry(self, False)

        for geom in self.m_flat_geoms:
            self.saveVertexData(geom)

        for geom in self.m_geoms:
            self.saveVertexData(geom)

    def rCollectGeometry(self, node: PandaNode, flat: bool):
        flat = flat or node.get_tag("flat_sea") == "true"

        if node.is_of_type(GeomNode.get_class_type()):
            geom_node = node
            for i in range(geom_node.get_num_geoms()):
                geom = geom_node.modify_geom(i)
                data = geom.modify_vertex_data()

                if flat:
                    self.m_flat_geoms.append(data)
                else:
                    self.m_geoms.append(data)

        for i in range(node.get_num_children()):
            self.rCollectGeometry(node.get_child(i), flat)

    def saveVertexData(self, data: GeomVertexData):
        array = GeomVertexArrayFormat()
        array.add_column(InternalName.get_color(), 4, Geom.NT_float32, Geom.C_color)
        array.add_column(InternalName.get_vertex(), 3, Geom.NT_float32, Geom.C_point)
        array.add_column(InternalName.get_normal(), 3, Geom.NT_float32, Geom.C_vector)
        array.add_column(InternalName.get_texcoord(), 2, Geom.NT_float32, Geom.C_texcoord)

        new_format = GeomVertexFormat()
        new_format.add_array(array)
        registered_format = GeomVertexFormat.register_format(new_format)
        data.set_format(registered_format)

    def doFlat(self, geom: GeomVertexData, anchor_mat, center_mat, anchor_rel_mat, current_thread):
        uv = GeomVertexWriter(geom, "texcoord", current_thread)
        normal = GeomVertexWriter(geom, "normal", current_thread)
        reflect = GeomVertexWriter(geom, "texcoord.reflect", current_thread)
        color = GeomVertexWriter(geom, "color", current_thread)
        reader = GeomVertexRewriter(geom, "vertex", current_thread)

        while not reader.is_at_end():
            vertex = reader.get_data3f()
            transformed_vertex = anchor_mat.xform_point(vertex)

            if self.m_want_z:
                z = self.m_z_offset + self.m_root.getSeaLevel()
                vertex = LPoint3f(vertex[0], vertex[1], z)
                reader.set_data3f(vertex)

            if self.m_want_normal:
                normal.set_data3f(LVecBase3f(0, 0, 1))

            if self.m_want_reflect:
                reflection_point = anchor_rel_mat.xform_point(transformed_vertex)
                up_vector = anchor_rel_mat.xform_vec(LVecBase3f(0, 0, 1))
                reflection_vector = LVecBase3f()
                self.calcReflection(up_vector, reflection_point, reflection_vector)
                reflect.set_data2f(reflection_vector[0] * 0.5 + 0.5, 0.5 - reflection_vector[2] * 0.5)

            if self.m_want_color:
                color.set_data4f(self.m_root.getMidColor())

            if self.m_want_uv:
                center_transformed = center_mat.xform_point(vertex)
                distance_squared = center_transformed.length_squared()
                uv_coords = self.m_root.calcUv(transformed_vertex[0], transformed_vertex[1], distance_squared)
                uv.set_data2f(uv_coords)

    def doWave(self, geom: GeomVertexData, anchor_mat, center_mat, anchor_rel_mat, current_thread):
        uv = GeomVertexWriter(geom, "texcoord", current_thread)
        normal = GeomVertexWriter(geom, "normal", current_thread)
        reflect = GeomVertexWriter(geom, "texcoord.reflect", current_thread)
        color = GeomVertexWriter(geom, "color", current_thread)
        reader = GeomVertexRewriter(geom, "vertex", current_thread)

        while not reader.is_at_end():
            vertex = reader.get_data3f()
            anchor_transformed = anchor_mat.xform_point(vertex)
            center_transformed = center_mat.xform_point(vertex)

            distance_squared = center_transformed.length_squared()
            height = self.m_root.calcHeight(anchor_transformed[0], anchor_transformed[1], distance_squared)

            if self.m_want_z:
                z = self.m_z_offset + height
                vertex = LPoint3f(vertex[0], vertex[1], z)
                reader.set_data3f(vertex)

            if self.m_want_normal or self.m_want_reflect:
                normal_vector = self.m_root.calcNormal(height, anchor_transformed[0], anchor_transformed[1], distance_squared)
                if self.m_want_normal:
                    normal.set_data3f(normal_vector)

                if self.m_want_reflect:
                    reflection_point = anchor_rel_mat.xform_point(anchor_transformed)
                    normal_transformed = anchor_rel_mat.xform_vec(normal_vector)
                    reflection_vector = LVecBase3f()
                    self.calcReflection(normal_transformed, reflection_point, reflection_vector)
                    reflect.set_data2f(reflection_vector[0] * 0.5 + 0.5, 0.5 - reflection_vector[2] * 0.5)

            if self.m_want_color:
                color.set_data4f(self.m_root.calcColor(height, anchor_transformed[0], anchor_transformed[1]))

            if self.m_want_uv:
                uv_coords = self.m_root.calcUv(anchor_transformed[0], anchor_transformed[1], distance_squared)
                uv.set_data2f(uv_coords)