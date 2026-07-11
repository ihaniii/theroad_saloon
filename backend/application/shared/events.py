from typing import Callable, List, Dict

class DomainEvent:
    pass

class EventPublisher:
    _subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_name: str, handler: Callable):
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []
        cls._subscribers[event_name].append(handler)

    @classmethod
    def publish(cls, event: DomainEvent):
        event_name = event.__class__.__name__
        handlers = cls._subscribers.get(event_name, [])
        for handler in handlers:
            handler(event)

    @classmethod
    def clear_subscribers(cls):
        cls._subscribers = {}
