from django.urls import path

from frontend.views.auth import (
    login,
    logout,
    register,
    account_uinfo,
    update_pincode,
    update_gpg,
    update_password,
    forget_password,
    before_login,
    update_user_photo
)
from frontend.views.goods import (
    goods_detail,
    goods_list,
    goods_collect,
    goods_collect_list,
    del_goods_collect
)
from frontend.views.index import index
from frontend.views.marchant import (
    marchants_detail,
    marchants_list,
    become_marchant,
    open_marchant,
    self_marchant_detail,
    marchant_add_goods,
    marchant_upd_goods,
    marchant_goods_list,
    marchant_goods_sale,
    update_marchant,
    marchant_order_list,
    marchant_order_detail,
    marchant_send_goods,
    agree_return_goods,
    refuse_return_goods,
    confirm_return_money,
    marchant_comment_list,
    user_marchant_detail,
    marchant_black_list,
    add_mct_to_blacklist,
    collect_marchant,
    collect_list,
    del_collect,
    del_black,
    marchant_settle_flow,
    create_marchant,
    goods_images_update,
    delele_goods_image
)
from frontend.views.order import (
    pay_order_info,
    create_pay_order,
    order_detail,
    order_list,
    return_order,
    cancle_return_order,
    return_orde_approval,
    set_orde_shipnum,
    confirm_recv_goods,
    del_order
)
from frontend.views.address import (
    address_list,
    update_address,
    add_address,
    del_address
)
from frontend.views.message import message_list, send_msg
from frontend.views.comment import create_comment
from frontend.views.forum import (
    forum_cat_list,
    forum_topic_list,
    forum_list_by_topic,
    forum_cmt_reply,
    forum_detail,
    pulish_form
)
from frontend.views.help_desk import (
    help_desk_detail,
    help_desk_list,
    submit_hd,
    hd_reply
)
from frontend.views.wallet import (
    wallet_info,
    wallet_record,
    wallet_withdraw,
    wallet_deposit,
    wallet_trans_record
)
from frontend.views.news import news_list, news_detail
from frontend.views.enter import enter_website
from frontend.views.wallet_chain import withdraw_deposit_notify

urlpatterns = [
    # 首页
    path(r"", enter_website, name="enter_website"),
    path(r"index", index, name="index"),

    # 用户模块相关的内容
    path(r"login", login, name="login"),
    path(r"register", register, name="register"),
    path(r"logout", logout, name="logout"),
    path(r"account_uinfo", account_uinfo, name="account_uinfo"),
    path(r"update_pincode", update_pincode, name="update_pincode"),
    path(r"update_gpg", update_gpg, name="update_gpg"),
    path(r"update_password", update_password, name="update_password"),
    path(r"forget_password", forget_password, name="forget_password"),
    path(r"before_login", before_login, name="before_login"),
    path(r"update_user_photo", update_user_photo, name="update_user_photo"),

    # 商品模块
    path(r"goods_list", goods_list, name="goods_list"),
    path(r"<int:id>/goods_detail", goods_detail, name="goods_detail"),
    path(r"goods_collect_list", goods_collect_list, name="goods_collect_list"),
    path(r"<int:gid>/goods_collect", goods_collect, name="goods_collect"),
    path(r"<int:gid>/del_goods_collect", del_goods_collect, name="del_goods_collect"),

    # 消息模块
    path(r"message_list", message_list, name="message_list"),
    path(r"send_msg", send_msg, name="send_msg"),

    # 商家模块
    path(r"marchants_list", marchants_list, name="marchants_list"),
    path(r"<int:id>/marchants_detail", marchants_detail, name="marchants_detail"),
    path(r"self_marchant_detail", self_marchant_detail, name="self_marchant_detail"),
    path(r"become_marchant", become_marchant, name="become_marchant"),
    path(r"open_marchant", open_marchant, name="open_marchant"),
    path(r"marchant_add_goods", marchant_add_goods, name="marchant_add_goods"),
    path(r"<int:gid>/marchant_upd_goods", marchant_upd_goods, name="marchant_upd_goods"),
    path(r"marchant_goods_list", marchant_goods_list, name="marchant_goods_list"),
    path(r"marchant_goods_sale", marchant_goods_sale, name="marchant_goods_sale"),
    path(r"<int:mid>/update_marchant", update_marchant, name="update_marchant"),
    path(r"<int:mid>/marchant_order_list", marchant_order_list, name="marchant_order_list"),
    path(r"<int:oid>/marchant_order_detail", marchant_order_detail, name="marchant_order_detail"),
    path(r"<int:oid>/marchant_send_goods", marchant_send_goods, name="marchant_send_goods"),
    path(r"<int:oid>/agree_return_goods", agree_return_goods, name="agree_return_goods"),
    path(r"<int:oid>/refuse_return_goods", refuse_return_goods, name="refuse_return_goods"),
    path(r"<int:oid>/confirm_return_money", confirm_return_money, name="confirm_return_money"),
    path(r"<int:mid>/marchant_comment_list", marchant_comment_list, name="marchant_comment_list"),
    path(r"<int:mid>/user_marchant_detail", user_marchant_detail, name="user_marchant_detail"),
    path(r"marchant_black_list", marchant_black_list, name="marchant_black_list"),
    path(r"<int:mid>/add_mct_to_blacklist", add_mct_to_blacklist, name="add_mct_to_blacklist"),
    path(r"<int:mid>/collect_marchant", collect_marchant, name="collect_marchant"),
    path(r"collect_list", collect_list, name="collect_list"),
    path(r"<int:id>/del_collect", del_collect, name="del_collect"),
    path(r"<int:id>/del_black", del_black, name="del_black"),
    path(r"<int:mid>/marchant_settle_flow", marchant_settle_flow, name="marchant_settle_flow"),
    path(r"create_marchant", create_marchant, name="create_marchant"),
    path(r"goods_images_update", goods_images_update, name="goods_images_update"),
    path(r"<int:gid>/delele_goods_image", delele_goods_image, name="delele_goods_image"),

    # 地址
    path(r"address_list", address_list, name="address_list"),
    path(r"add_address", add_address, name="add_address"),
    path(r"<int:aid>/update_address", update_address, name="update_address"),
    path(r"<int:aid>/del_address", del_address, name="del_address"),

    # 论坛
    path(r"forum_cat_list", forum_cat_list, name="forum_cat_list"),
    path(r"<int:fid>/forum_topic_list", forum_topic_list, name="forum_topic_list"),
    path(r"<int:fid>/forum_list_by_topic", forum_list_by_topic, name="forum_list_by_topic"),
    path(r"<int:fid>/forum_detail", forum_detail, name="forum_detail"),
    path(r"<int:fid>/forum_cmt_reply", forum_cmt_reply, name="forum_cmt_reply"),
    path(r"pulish_form", pulish_form, name="pulish_form"),

    # 订单
    path(r"pay_order_info", pay_order_info, name="pay_order_info"),
    path(r"order_list", order_list, name="order_list"),
    path(r"create_pay_order", create_pay_order, name="create_pay_order"),
    path(r"<int:id>/order_detail", order_detail, name="order_detail"),
    path(r"<int:oid>/return_order", return_order, name="return_order"),
    path(r"<int:oid>/cancle_return_order", cancle_return_order, name="cancle_return_order"),
    path(r"<int:oid>/return_orde_approval", return_orde_approval, name="return_orde_approval"),
    path(r"<int:oid>/set_orde_shipnum", set_orde_shipnum, name="set_orde_shipnum"),
    path(r"<int:oid>/confirm_recv_goods", confirm_recv_goods, name="confirm_recv_goods"),
    path(r"<int:oid>/del_order", del_order, name="del_order"),

    # 工单模块
    path(r"help_desk_list", help_desk_list, name="help_desk_list"),
    path(r"<int:top_id>/help_desk_detail", help_desk_detail, name="help_desk_detail"),
    path(r"submit_hd", submit_hd, name="submit_hd"),
    path(r"hd_reply", hd_reply, name="hd_reply"),

    # 评论
    path(r"<int:oid>/create_comment", create_comment, name="create_comment"),

    # 钱包模块
    path(r"wallet_info", wallet_info, name="wallet_info"),
    path(r"wallet_record", wallet_record, name="wallet_record"),
    path(r"wallet_withdraw", wallet_withdraw, name="wallet_withdraw"),
    path(r"wallet_deposit", wallet_deposit, name="wallet_deposit"),
    path(r"wallet_trans_record", wallet_trans_record, name="wallet_trans_record"),

    # 消息公告
    path(r"news_list", news_list, name="news_list"),
    path(r"<int:nid>/news_detail", news_detail, name="news_detail"),

    # 钱包上账模块
    path(r"withdraw_deposit_notify", withdraw_deposit_notify, name="withdraw_deposit_notify"),
]
