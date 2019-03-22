from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import qiniu.config

# 需要填写你的Access Key和Secret Key
access_key = 'eP-3L0DMcgblVbrP3pI_t49KmaDzYIL5xYF_nIss'
secret_key = 'UWc8zPErpqVDJLdItCxncT46Y-D93DTCiu73gfNl'

def storage(file_data):
    '''
    上传文件到七牛
    :param file_data: 要上传的数据
    :return:
    '''
    # 构建鉴权对象
    q=Auth(access_key,secret_key)

    # 要上传的空间名字
    bucket_name='ihome-python'

    # 生成上传Token,可以指定过期时间等
    token=q.upload_token(bucket_name,None,3600)

    ret,info=put_data(token,None,file_data)
    print(info)
    print("*"*10)
    print(ret)
    if info.status_code == 200:
        # 表示上传成功 返回文件名
        return ret.get("key")
    else:
        # 上传失败
        raise Exception("上传文件失败")


if __name__ == '__main__':
    storage()

