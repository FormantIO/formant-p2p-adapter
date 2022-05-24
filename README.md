# Formant p2p adapter

This creates an http interface that enables webRTC connections with a robot running the formant agent. In order for webRTC network exchange to work it must have a valid HTTPS frontend and backend. Generate your certificate using `./gen_cert.sh`.

Install requirements and run your adapter with `./start.sh`


By default it runs on `https://localhost:8000`. If you use our data-sdk, this should be url you `Fleet.getPeerDevice("https://localhost:8000")` with.

Check out https://github.com/FormantIO/toolkit/edit/master/examples/teleop-peer for an example of a frontend that can run on this.
