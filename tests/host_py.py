
from bindings import WasiCe
import sys
import wasmtime

from cloudevents.http import CloudEvent, to_structured
import requests

from bindings import Err


def run(cloudevent: CloudEvent) -> None:
    store = wasmtime.Store()
    module = wasmtime.Module.from_file(store.engine, "crates/ce/target/wasm32-wasi/release/ce.wasm")
    linker = wasmtime.Linker(store.engine)
    linker.define_wasi()
    wasi = wasmtime.WasiConfig()
    wasi.inherit_stdout()
    wasi.inherit_stderr()
    store.set_wasi(wasi)
    wasm = WasiCe(store, linker, module)

    header, body = to_structured(cloudevent)
    body = body.decode("utf-8")

    res = wasm.ce_handler(store, body)
    
    

if __name__ == "__main__":
    # Create a CloudEvent
    # - The CloudEvent "id" is generated if omitted. "specversion" defaults to "1.0".
    attributes = {
        "type": "com.microsoft.steelthread.wasm",
        "source": "https://example.com/event-producer",
    }
    data = "hello world"
    event = CloudEvent(attributes, data)
    run(event)