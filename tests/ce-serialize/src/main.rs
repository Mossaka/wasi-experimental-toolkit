use cloudevents::{EventBuilder, EventBuilderV10, Event};
use serde::ser::{Serialize, Serializer};

fn main() {
    println!("Hello, world!");
    use url::Url;

    let event = EventBuilderV10::new()
        .id("aaa")
        .source(Url::parse("http://localhost").unwrap())
        .ty("example.demo")
        .data("bytes", "hello world")
        .build().unwrap();

    let s = serde_json::to_string(&event).unwrap();

    println!("{}", s);

    let event_: Event = serde_json::from_str(s.as_str()).unwrap();
    println!("{}", serde_json::to_string(&event_).unwrap());
}
