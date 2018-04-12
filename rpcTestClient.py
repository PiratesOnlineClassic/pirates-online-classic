import rpyc

conn = rpyc.connect('127.0.0.1', 19912)
conn.root.authenticate('test_token')
print(conn.root.systemMessage('Hello world!'))
print(conn.root.ping('Pong'))