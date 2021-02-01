# import os
# import sys
# from bitcoin.networks import NETWORKS
# from bitcoin.bip32 import HDKey


# class Persistence:
#     MASTER_XPUB_FILE_PATH = "master_xpub.txt"
#     NETWORK_FILE_PATH = "network.txt"
#     RECOVERY_PHRASE_LENGTH_FILE_PATH = "recovery_phrase_length.txt"

#     @classmethod
#     def load_master_xpub(cls):
#         if cls.MASTER_XPUB_FILE_PATH in os.listdir():
#             with open(cls.MASTER_XPUB_FILE_PATH, "r", encoding="utf-8") as f:
#                 master_xpub_str = f.read()
#                 return HDKey.from_base58(master_xpub_str)
#         return None

#     @classmethod
#     def save_master_xpub(cls, master_xpub):
#         master_xpub_str = master_xpub.to_base58()
#         with open(cls.MASTER_XPUB_FILE_PATH, "w",  encoding="utf-8") as f:
#             f.write(master_xpub_str)

#     @classmethod
#     def load_network(cls):
#         if cls.NETWORK_FILE_PATH in os.listdir():
#             with open(cls.NETWORK_FILE_PATH, "r") as f:
#                 return f.read()
#         return None

#     @classmethod
#     def save_network(cls, network: str):
#         with open(cls.NETWORK_FILE_PATH, "w") as f:
#             f.write(network)

#     @classmethod
#     def load_recovery_phrase_length(cls) -> int:
#         if cls.RECOVERY_PHRASE_LENGTH_FILE_PATH in os.listdir():
#             with open(cls.RECOVERY_PHRASE_LENGTH_FILE_PATH, "r") as f:
#                 return int(f.read())
#         return None

#     @classmethod
#     def save_recovery_phrase_length(cls, recovery_phrase_length: int):
#         with open(cls.RECOVERY_PHRASE_LENGTH_FILE_PATH, "w") as f:
#             f.write(str(recovery_phrase_length))

#     # @classmethod
#     # def _save_debug(cls, log: str, file_name: str):
#     #     with open(file_name, "w+") as f:
#     #         f.write(log)
