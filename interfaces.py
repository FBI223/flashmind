from abc import ABC, abstractmethod

class ITimerApp(ABC):

    @abstractmethod
    def update_timer(self):
        pass

    @abstractmethod
    def destroy(self):
        pass