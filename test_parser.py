import unittest
from parser import parse_message, parse_messages

class ParserCase(unittest.TestCase):
    def setUp(self):
        # Messages are - alert message using LBS, alert message using GPS, normal message to SMS/webserver
        self.messages = [
            "*TS01,861585041322775,191337200220,LBS:730;1;3337;3E4B02;69,STT:242;0,\
MGR:183389,ADC:0;11.57;1;27.27;2;3.44,GFS:0;0,OBD:310539410C3002310D68312F80,\
FUL:6886859,HDB:8,VIN:1G1JC5444R7252367,EGT:11295,EVT:F0;242#",
            "*TS01,861585041322775,192312200220,GPS:3;S33.442064;W70.612964;93;42;0.85\
,STT:252;0,MGR:192375,ADC:0;11.56;1;38.32;2;3.79,GFS:1;1,OBD:310539410C2CD2310D5D312F80,\
FUL:6950158,EGT:11871,EVT:80;1#",
            "*TS01,861585040983700,201910130120,GPS:2;S33.440978;W70.612985;0;0;3.02,\
STT:0;0,MGR:0,ADC:0;12.70;1;36.64;2;4.20,EVT:0#"
        ]
        self.message = "*TS01,861585040983700,201910130120,GPS:2;S33.440978;W70.612985;0;0;3.02,\
STT:0;0,MGR:0,ADC:0;12.70;1;36.64;2;4.20,EVT:0#"

    def test_one_message(self):
        ## assuming only one message will be sent by the obd
        parsed_message = parse_message(self.message)
        print(parsed_message)
        self.assertIsInstance(parsed_message, dict)
        self.assertEqual(parsed_message['protocol'], '01')
        self.assertEqual(parsed_message['device_id'], '861585040983700')
        self.assertEqual(parsed_message['timestamp'], '201910130120')

    def test_invalid_message(self):
        # message without header
        parsed_message = parse_message(self.message[1:])
        self.assertIsInstance(parsed_message, dict)
        self.assertIn('error', parsed_message)
        self.assertEqual(parsed_message['error'], "invalid message")
        
        # message without tail
        parsed_message = parse_message(self.message[:-1])
        self.assertIsInstance(parsed_message, dict)
        self.assertIn('error', parsed_message)
        self.assertEqual(parsed_message['error'], "invalid message")

        #random string
        parsed_message = parse_message("Czk9cQyp2hiQSe1wsO0m")
        self.assertIsInstance(parsed_message, dict)
        self.assertIn('error', parsed_message)
        self.assertEqual(parsed_message['error'], "invalid message")

    def test_messsages(self):
        message_list = parse_messages(self.messages)
        self.assertIsInstance(message_list, list)
        self.assertEqual(len(message_list), 3)
        for message in message_list:
            self.assertIn('protocol', message)
            self.assertIn('device_id', message)
            self.assertIn('timestamp', message)

    def test_messages_with_errors(self):
        # incomplete message
        self.messages.append(",GPS:2;S33.440978;W70.612985;0;0;3.02,\
STT:0;0,MGR:0,ADC:0;12.70;1;36.64;2;4.20,EVT:")
        # random garbage
        self.messages.append("CYgJaChfrNUFnYEup7Hk")
        # message without head
        self.messages.append(self.message[1:])
        # message without tail
        self.messages.append(self.message[:-1])

        message_list = parse_messages(self.messages) # bad messages should be filtered out
        self.assertIsInstance(message_list, list)
        self.assertEqual(len(message_list), 3)
        for message in message_list:
            self.assertIn('protocol', message)
            self.assertIn('device_id', message)
            self.assertIn('timestamp', message)
