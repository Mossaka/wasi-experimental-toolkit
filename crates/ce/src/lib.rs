wit_bindgen_rust::export!("../../wit/ephemeral/wasi-ce.wit");

use wasi_ce::*;
use cloudevents::{Event, AttributesReader};


struct WasiCe {}

impl wasi_ce::WasiCe for WasiCe {
    fn ce_handler(event: String) -> Result<String,Error> {
        let event_: Event = serde_json::from_str(event.as_str()).unwrap();
        println!("event id: {}", event_.id());
        Ok(event)
    }
}

// TODO
// Error handling is currently not implemented.
impl From<anyhow::Error> for Error {
    fn from(_: anyhow::Error) -> Self {
        Self::Error
    }
}

impl From<std::io::Error> for Error {
    fn from(_: std::io::Error) -> Self {
        Self::Error
    }
}
