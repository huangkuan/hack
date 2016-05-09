curl -H "Content-Type: application/json" -X POST -d '{"t":"t"}' http://127.0.0.1:8080/kikapi_config

curl -H "Content-Type: application/json" -X POST -d '{"messages":"asdf"}' http://127.0.0.1:8080/kikapi_config
curl -H "Content-Type: application/json" -X POST -d '{"messages":[{"body":"kik welcome"}]}' http://127.0.0.1:8080/kikapi_receivemsg


curl -H "Content-Type: application/json" -X POST -d '{"t":"t"}' https://kikapi-1298.appspot.com/kikapi_config


Installing 3rd party library for webapp2 app. You need to install it to "lib" folder
pip install -t lib -r requirements.txt


local serverdev_appserver.py .



WIT
curl -H 'Authorization: Bearer 26WCUF6D6T2KL6FOH2PEK2HNXDIU2EZ3' -H 'Accept: application/vnd.wit.20141022+json' 'https://api.wit.ai/message?q=hello'




{u'outcomes': [{u'entities': {u'location': [{u'suggested': True, u'type': u'value', u'value': u'London'}]}, u'confidence': None, u'intent': u'default_intent', u'_text': u'weather in London'}], u'msg_id': u'6163c069-fd44-4287-b6b3-f7fa2a1d4305', u'_text': u'weather in London'}

Sample FB Message:

text
{"object":"page","entry":
	[{
	"id":510512709009335,
	"time":1462830984780,
	"messaging":
		[
			{
			"sender":{
					"id":353463854777868
			},
			"recipient":{
				"id":510512709009335
			},

			"timestamp":1462830984715,
			"message":{
				"mid":"mid.1462830984670:67a9aebe4cecfdb528",
				"seq":4,
				"text":"Ahaha"}
			}
		]
	}]
}


voice
{"object":"page","entry":[{"id":510512709009335,"time":1462831049724,"messaging":[{"sender":{"id":353463854777868},"recipient":{"id":510512709009335},"timestamp":1462831049679,"message":{"mid":"mid.1462831049027:d61f3f3cee6d27d966","seq":5,"attachments":[{"type":"audio","payload":{"url":"https:\/\/cdn.fbsbx.com\/v\/t59.3654-21\/13125087_10104925638592579_341428229_n.mp4\/audioclip-1462831048000-1756.mp4?oh=4925c871f85f1669fcb53a3451699a80&oe=57328D24"}}]}}]}]}

Like button
{"object":"page","entry":[{"id":510512709009335,"time":1462831405538,"messaging":[{"sender":{"id":353463854777868},"recipient":{"id":510512709009335},"timestamp":1462831405505,"message":{"mid":"mid.1462831405486:364cfbaa7c57df3308","seq":10,"sticker_id":369239343222814,"attachments":[{"type":"image","payload":{"url":"https:\/\/fbcdn-dragon-a.akamaihd.net\/hphotos-ak-xaf1\/t39.1997-6\/p100x100\/851587_369239346556147_162929011_n.png"}}]}}]}]}

Location
{"object":"page","entry":[{"id":510512709009335,"time":1462831442791,"messaging":[{"sender":{"id":353463854777868},"recipient":{"id":510512709009335},"timestamp":1462831442741,"message":{"mid":"mid.1462831442528:9f35630223d18bc236","seq":11,"attachments":[{"title":"Kuan's Location","url":"https:\/\/www.facebook.com\/l.php?u=https\u00253A\u00252F\u00252Fwww.bing.com\u00252Fmaps\u00252Fdefault.aspx\u00253Fv\u00253D2\u002526pc\u00253DFACEBK\u002526mid\u00253D8100\u002526where1\u00253D40.740507163823\u0025252C\u00252B-74.007804460413\u002526FORM\u00253DFBKPL1\u002526mkt\u00253Den-US&h=EAQG0dFKN&s=1&enc=AZPdTGPTgIENGH8thj31euZwBastoyAJmgmGJJ3SYjb14Acx17B8M6AmZcyyOunvhZqAlnzcbdrBpNaG7jD99D4jnesLYnjACpDDEfsXob6GrQ","type":"location","payload":{"coordinates":{"lat":40.740507163823,"long":-74.007804460413}}}]}}]}]}

GIF
{"object":"page","entry":[{"id":510512709009335,"time":1462831482668,"messaging":[{"sender":{"id":353463854777868},"recipient":{"id":510512709009335},"timestamp":1462831482619,"message":{"mid":"mid.1462831482470:641b8d9eacb6ecc331","seq":12,"attachments":[{"type":"image","payload":{"url":"https:\/\/cdn.fbsbx.com\/v\/t59.2708-21\/11988983_1068775179808982_479777370_n.gif?oh=0df1bb137b0643533cb4017492d199da&oe=57334918"}}]}}]}]}


## E2E Test for this sample app

A Makefile is provided to deploy and run the e2e test.

To run:

     export GAE_PROJECT=your-project-id
     make

To manually run, install the requirements

    pip install -r e2e/requirements-dev.txt

Set the environment variable to point to your deployed app:

    export GUESTBOOK_URL="http://guestbook-test-dot-useful-temple-118922.appspot.com/"

Finally, run the test

    python e2e/test_e2e.py
