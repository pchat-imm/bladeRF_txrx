**date:** 27/01/25
**purpose:** use keysight to recieve signal from sdr that transmit PSS seq (0,1,2)
- center freq 3.5 GHz
- recommend gain is at least 30 dB (range -15 to 60 dB) 
- with multiple repeat (rep) like 200


**result**
- all peaks occur in 3.5 GHz (3.5 GHz, 3.5009 GHz, 3.501 GHz)
- even the same PSS seq, can have different results as we use repeat
- don't see the different between PSS seq yet (0,1,2)
- in RTSA (Real-time Spectrum Analyzer), show two peaks that changed two time
- in SA spectrum, show three locations
- in SA waterfall, can show two locations, or three
