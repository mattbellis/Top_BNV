python -u test_genparticle_tracing_v2.py /home/bellis/top_data/NANOAOD/Reza_signal/nAOD_step_BNV_TT_TSUE/NAOD-00000_198.root --event-range 0,25000      >& log1.log &
python -u test_genparticle_tracing_v2.py /home/bellis/top_data/NANOAOD/Reza_signal/nAOD_step_BNV_TT_TSUE/NAOD-00000_198.root --event-range 25000,50000  >& log2.log &
python -u test_genparticle_tracing_v2.py /home/bellis/top_data/NANOAOD/Reza_signal/nAOD_step_BNV_TT_TSUE/NAOD-00000_198.root --event-range 50000,75000  >& log3.log &
python -u test_genparticle_tracing_v2.py /home/bellis/top_data/NANOAOD/Reza_signal/nAOD_step_BNV_TT_TSUE/NAOD-00000_198.root --event-range 75000,100000 >& log4.log &
