class PumpModel(object):
    def run(self):
        try:
            self._start()
            self._pump()
        finally:
            self._end()

    def _start(self):
        pass

    def _pump(self):
        pass

    def _end(self):
        pass
