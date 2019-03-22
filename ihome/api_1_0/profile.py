
from . import api
from ihome.utils.commons import login_required
from flask import g,current_app,jsonify,request,session
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import User
from ihome import db,constants


@api.route("/users/avatar",methods=["POST"])
@login_required
def set_user_avatar():
    '''设置用户的头像
    参数：图片（多媒体表单格式）用户id（g.user_id)
    '''
    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接获取
    user_id=g.user_id

    # 获取图片
    image_file=request.files.get("avatar")

    if image_file is None:
        return jsonify(errno=RET.PARAMERR,errmsg="未上传图片")

    image_data=image_file.read()

    # 调用七牛上传图片 返回文件名
    try:
        file_name=storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg="上传图片失败")

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar_url":file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存图片信息失败")

    avatar_url = constants.QINIU_URL_DOMAIN + file_name
    # 保存成功返回
    return jsonify(errno=RET.OK,errmsg="保存成功",data={"file_name":avatar_url})


@api.route("/users/name",methods=["PUT"])
@login_required
def change_user_name():
    '''修改用户名'''
    # 使用了login_required装饰器后，可以从g对象中获取用户user_id
    user_id=g.user_id

    # 获取用户想要设置的用户名
    req_data=request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    name=req_data.get("name")  # 用户想要设置的名字
    if not name:
        return jsonify(errno=RET.PARAMERR,errmsg="名字不能为空")

    # 保存用户昵称name，并同时判断name是否重复（利用数据库的唯一索引）
    try:
        User.query.filter_by(id=user_id).update({"name":name})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="设置用户昵称错误")

    # 修改session数据中的name字段
    session["name"]=name
    return jsonify(errno=RET.OK,errmsg="OK",data={"name":name})


@api.route("/user",methods=["GET"])
@login_required
def get_user_profile():
    '''获取个人信息'''
    user_id=g.user_id

    # 查询数据库获取个人信息
    try:
        user=User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA,errmsg="获取用户信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA,errmsg="无效操作")

    return jsonify(errno=RET.OK,errmsg="OK",data=user.to_dict())


@api.route("/users/auth", methods=["GET"])
@login_required
def get_user_auth():
    """获取用户的实名认证信息"""
    user_id = g.user_id

    # 在数据库中查询信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户实名信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


@api.route("/users/auth", methods=["POST"])
@login_required
def set_user_auth():
    """保存实名认证信息"""
    user_id = g.user_id

    # 获取参数
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    real_name = req_data.get("real_name")  # 真实姓名
    id_card = req_data.get("id_card")  # 身份证号

    # 参数校验
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 保存用户的姓名与身份证号
    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None)\
            .update({"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存用户实名信息失败")

    return jsonify(errno=RET.OK, errmsg="OK")