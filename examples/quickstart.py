from unsteady_flow.analysis import summarize_temporal_signal
from unsteady_flow.signals import damped_tone


signal = damped_tone(frequency=5_000, damping_rate=500)
print(summarize_temporal_signal(signal))
