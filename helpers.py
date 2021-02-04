import io
import pickle
import pprint

import cloudpickle
import ipfshttpclient

pp = pprint.pprint


def get_blocks(cid, depth=0):
    result = []
    objects = client.ls(cid)["Objects"]
    links = objects[0]["Links"]
    if len(links) == 0:
        return [objects[0]["Hash"]]
    for link in links:
        result.extend(get_blocks(link["Hash"]))
    return result


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
