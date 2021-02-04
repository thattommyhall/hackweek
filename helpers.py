import io
import pickle
import pprint

import cloudpickle
import ipfshttpclient

pp = pprint.pprint


def ipfs_cat(cid):
    client = ipfshttpclient.connect()
    data = client.cat(cid)
    try:
        return cloudpickle.loads(data)
    except Exception:
        return data


def ipfs_pickle(obj):
    with io.BytesIO() as tmp_file:
        tmp_file.write(cloudpickle.dumps(obj))
        tmp_file.flush()
        tmp_file.seek(0)
        client = ipfshttpclient.connect()
        res = client.add(tmp_file)
        return res["Hash"]


def ipfs_call(fn_cid, arg_cid):
    f = ipfs_cat(fn_cid)
    arg = ipfs_cat(arg_cid)
    result = f(arg)
    return ipfs_pickle(result)
