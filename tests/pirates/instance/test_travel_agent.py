import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from pirates.instance.DistributedTravelAgentAI import DistributedTravelAgentAI
from pirates.instance.DistributedTravelAgentUD import DistributedTravelAgentUD
from pirates.distributed.DistrictTrackerAI import DistrictTrackerAI
from pirates.piratesbase import PiratesGlobals


class DistrictTrackerAITests(unittest.TestCase):

    def test_status_reports_shard_type_to_the_uberdog(self):
        tracker = DistrictTrackerAI.__new__(DistrictTrackerAI)
        tracker.air = SimpleNamespace(
            populationTracker=SimpleNamespace(
                getShardId=lambda: 2,
                getPopulation=lambda: 4,
                getPopLimits=lambda: (10, 20)),
            distributedDistrict=SimpleNamespace(
                getShardType=lambda: PiratesGlobals.SHARD_MAIN,
                getName=lambda: 'Test District'),
            newsManager=SimpleNamespace(holidayList={}),
            netMessenger=SimpleNamespace(send=Mock()),
            ourChannel=300)
        tracker.populationTracker = tracker.air.populationTracker
        tracker.district = tracker.air.distributedDistrict
        tracker.newsManager = tracker.air.newsManager

        tracker.sendDistrictStatusQuery()

        status = tracker.air.netMessenger.send.call_args.args[1][1]
        self.assertEqual(status['shardType'], PiratesGlobals.SHARD_MAIN)


class TravelAgentUDTests(unittest.TestCase):

    def makeAgent(self, shardStatuses):
        agent = DistributedTravelAgentUD.__new__(DistributedTravelAgentUD)
        agent._DistributedTravelAgentUD__shards = {
            channel: status['shardId'] for channel, status in shardStatuses.items()}
        agent.air = SimpleNamespace(
            districtTracker=SimpleNamespace(getShards=lambda: shardStatuses))
        agent.notify = Mock()
        agent.sendUpdateToChannel = Mock()
        return agent

    def test_automatic_cross_shard_deploy_selects_a_main_shard(self):
        agent = self.makeAgent({
            100: {'shardId': 1, 'shardType': PiratesGlobals.SHARD_WELCOME},
            200: {'shardId': 2, 'shardType': PiratesGlobals.SHARD_MAIN},
            300: {'shardId': 3, 'shardType': PiratesGlobals.SHARD_WELCOME},
        })

        agent.requestCrossShardDeployAItoUD(42, 1, 0, 'tortuga', 900)

        agent.sendUpdateToChannel.assert_called_once_with(
            200, 'requestCrossShardDeployUDtoAI', [42, 2, 'tortuga', 900])

    def test_missing_main_shard_fails_the_requesting_district(self):
        agent = self.makeAgent({
            100: {'shardId': 1, 'shardType': PiratesGlobals.SHARD_WELCOME},
            300: {'shardId': 3, 'shardType': PiratesGlobals.SHARD_WELCOME},
        })

        agent.requestCrossShardDeployAItoUD(42, 1, 0, 'tortuga', 900)

        agent.sendUpdateToChannel.assert_called_once_with(
            100, 'crossShardDeployFailed', [42])


class TravelAgentAITests(unittest.TestCase):

    def test_arrived_avatar_is_deployed_and_sent_to_the_ship(self):
        avatar = SimpleNamespace(doId=42)
        teleportMgr = SimpleNamespace(_handleLocalCrossShardDeploy=Mock())
        agent = DistributedTravelAgentAI.__new__(DistributedTravelAgentAI)
        agent.air = SimpleNamespace(
            districtId=2,
            doId2do={42: avatar},
            teleportMgr=teleportMgr)
        agent.notify = Mock()

        agent.requestCrossShardDeployUDtoAI(42, 2, 'tortuga', 900)

        teleportMgr._handleLocalCrossShardDeploy.assert_called_once_with(
            avatar, 'tortuga', 900)


if __name__ == '__main__':
    unittest.main()
