
from bindings import WasiCe
import sys
import wasmtime

from cloudevents.http import CloudEvent, to_binary
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

    # headers, body = to_binary(cloudevent)

    wasm = WasiCe(store, linker, module)
    event = str(cloudevent)

    res = wasm.ce_handler(store, event)
    
    event.drop(store)
    res.value.drop(store)
    
    

if __name__ == "__main__":
    # Create a CloudEvent
    # - The CloudEvent "id" is generated if omitted. "specversion" defaults to "1.0".
    attributes = {
        "type": "com.microsoft.steelthread.wasm",
        "source": "https://example.com/event-producer",
    }
    data = {"message": "Hello World!"}
    event = CloudEvent(attributes, data)
    run(event)