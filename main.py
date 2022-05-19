from fastapi import Request, Response, FastAPI
from fastapi.responses import JSONResponse
from formant.sdk.agent.v1 import Client as FormantClient
from google.protobuf.json_format import MessageToDict
from fastapi.middleware.cors import CORSMiddleware
from formant.protos.agent.v1 import agent_pb2


FRONTEND_ORIGIN = "https://myfrontenddomain.com"

app = FastAPI()
# connections = set()

fclient = FormantClient(
    ignore_throttled=True, ignore_unavailable=True, agent_url="localhost:5501",
)

dps = []


def handle_telemetry(datapoint):
    global dps
    dps.append(MessageToDict(datapoint))
    if len(dps) > 100:
        dps.pop(0)


# Handling data ...
fclient.register_telemetry_listener_callback(handle_telemetry, stream_filter=[])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:5000"],
    allow_methods=["GET", "POST"],
)


@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    origin = request.headers.get("Origin")
    response = Response()
    if origin is None:
        return response
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.get("/configuration")
async def status(request: Request):
    config_request = agent_pb2.GetAgentConfigurationRequest()
    agent_config = fclient.agent_stub.GetAgentConfiguration(config_request)
    return JSONResponse(
        content={"agent_config": MessageToDict(agent_config.configuration),}
    )


@app.post("/rtc-offer")
async def send_teleop_offer(request: Request):
    params = await request.json()
    config_request = agent_pb2.PostLanRtcOfferRequest(offer=params["offer"])
    agent_config = fclient.agent_stub.PostLanRtcOffer(config_request)
    return JSONResponse(content=MessageToDict(agent_config))


@app.get("/telemetry")
async def latest_telemtry(request: Request):
    global dps
    ret = dps.copy()
    dps = []
    return ret
