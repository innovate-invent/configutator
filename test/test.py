from configutator import ConfigMap, ArgMap, EnvMap, loadConfig
import sys

def test(param1: int, param2: str):
    print(param1, param2)

if __name__ == '__main__':
    for argMap in loadConfig(sys.argv, (test,), "Test"):
        test(argMap[test])

