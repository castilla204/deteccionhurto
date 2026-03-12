class FrameSampler:
    # YOLO es pesado; no tiene sentido correrlo en cada frame

    def __init__(self, process_every_n_frames=5):
        self.process_every_n_frames = process_every_n_frames
        self.frame_count = 0

    def should_process(self):
        self.frame_count += 1
        return self.frame_count % self.process_every_n_frames == 0
