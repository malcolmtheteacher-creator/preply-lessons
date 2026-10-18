"""All A2/B1 configs, keyed rp_NN. Family files register into CONFIGS_A2."""
from cfg_a2_util import REPAIR_A2  # noqa: F401
import cfg_a2_f1, cfg_a2_f2, cfg_a2_f3, cfg_a2_f4, cfg_a2_f5, cfg_a2_f6

CONFIGS_A2 = {}
for _m in (cfg_a2_f1, cfg_a2_f2, cfg_a2_f3, cfg_a2_f4, cfg_a2_f5, cfg_a2_f6):
    _m.register(CONFIGS_A2)
