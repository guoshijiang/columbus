from django.urls import path
from backend.views.control import (
    bar_index,
    bar_marchant,
    bar_goods,
    bar_help,
    bar_forum,
    bar_order,
    bar_wallet,
    bar_user
)
from backend.views.index import b_index
from backend.views.marchant import (
    b_marchants_list,
    b_marchant_detail,
    b_marchant_flow,
    open_marchant_list,
    disable_marchant,
    enable_marchant,
    update_mct_settle,
    marchant_cmt_data
)
from backend.views.goods import (
    b_goods_detail,
    b_goods_list,
    disable_goods,
    enable_goods,
    b_goods_comment_list,
    b_goods_cat,
    create_bgoods_cat,
    update_bgoods_cat,
    delete_bgoods_cat,
    b_goods_state,
    create_bgoods_state,
    update_bgoods_state,
    delete_bgoods_state
)
from backend.views.order import (
    b_order_list,
    b_order_detail,
    order_adjust
)
from backend.views.forum import (
    b_forum_cat,
    create_bforum_cat,
    update_bforum_cat,
    delete_bforum_cat,
    b_forum_topic,
    create_bforum_topic,
    update_bforum_topic,
    delete_bforum_topic,
    b_forum_list,
    b_forum_detail,
    b_forum_comment,
    disable_forum,
    enable_forum
)
from backend.views.config import (
    mct_config_list,
    create_mct_config,
    update_mct_config
)
from backend.views.help_center import (
    bnews_list,
    bnews_detail,
    create_bnews,
    update_bnews,
    delete_news,
    bhd_list,
    bhd_detail,
    bhd_reply,
    bhd_close
)
from backend.views.wallet import (
    coin_list,
    create_coin,
    update_coin,
    delete_coin,
    wd_list,
    trans_list,
)

from backend.views.user import (
    user_list,
    user_detail,
    user_wallets,
    user_recv_address,
    user_collect_mct,
    user_collect_gds,
    user_backlist_mct,
    disable_user,
    enable_user
)
from backend.views.login import b_login, b_logout

urlpatterns = [
    # 侧边导航栏控制
    path(r"bar_index", bar_index, name="bar_index"),
    path(r"bar_marchant", bar_marchant, name="bar_marchant"),
    path(r"bar_goods", bar_goods, name="bar_goods"),
    path(r"bar_help", bar_help, name="bar_help"),
    path(r"bar_forum", bar_forum, name="bar_forum"),
    path(r"bar_order", bar_order, name="bar_order"),
    path(r"bar_wallet", bar_wallet, name="bar_wallet"),
    path(r"bar_user", bar_user, name="bar_user"),

    # 后台首页
    path(r"", b_index, name="b_index"),

    # 用户模块
    path(r"user_list", user_list, name="user_list"),
    path(r"<int:uid>/user_detail", user_detail, name="user_detail"),
    path(r"<int:uid>/user_wallets", user_wallets, name="user_wallets"),
    path(r"<int:uid>/user_recv_address", user_recv_address, name="user_recv_address"),
    path(r"<int:uid>/user_collect_mct", user_collect_mct, name="user_collect_mct"),
    path(r"<int:uid>/user_collect_gds", user_collect_gds, name="user_collect_gds"),
    path(r"<int:uid>/user_backlist_mct", user_backlist_mct, name="user_backlist_mct"),
    path(r"<int:uid>/disable_user", disable_user, name="disable_user"),
    path(r"<int:uid>/enable_user", enable_user, name="enable_user"),

    # 钱包模块
    path(r"coin_list", coin_list, name="coin_list"),
    path(r"create_coin", create_coin, name="create_coin"),
    path(r"<int:cid>/update_coin", update_coin, name="update_coin"),
    path(r"<int:cid>/delete_coin", delete_coin, name="delete_coin"),
    path(r"wd_list", wd_list, name="wd_list"),
    path(r"trans_list", trans_list, name="trans_list"),

    # 商家模块
    path(r"b_marchants_list", b_marchants_list, name="b_marchants_list"),
    path(r"<int:mid>/b_marchant_detail", b_marchant_detail, name="b_marchant_detail"),
    path(r"b_marchant_flow", b_marchant_flow, name="b_marchant_flow"),
    path(r"open_marchant_list", open_marchant_list, name="open_marchant_list"),
    path(r"<int:mid>/disable_marchant", disable_marchant, name="disable_marchant"),
    path(r"<int:mid>/enable_marchant", enable_marchant, name="enable_marchant"),
    path(r"<int:mid>/update_mct_settle", update_mct_settle, name="update_mct_settle"),
    path(r"<int:mid>/marchant_cmt_data", marchant_cmt_data, name="marchant_cmt_data"),

    # 商品模块
    path(r"b_goods_list", b_goods_list, name="b_goods_list"),
    path(r"<int:gid>/b_goods_detail", b_goods_detail, name="b_goods_detail"),
    path(r"<int:gid>/disable_goods", disable_goods, name="disable_goods"),
    path(r"<int:gid>/enable_goods", enable_goods, name="enable_goods"),
    path(r"<int:gid>/b_goods_comment_list", b_goods_comment_list, name="b_goods_comment_list"),
    path(r"b_goods_cat", b_goods_cat, name="b_goods_cat"),
    path(r"create_bgoods_cat", create_bgoods_cat, name="create_bgoods_cat"),
    path(r"<int:cid>/update_bgoods_cat", update_bgoods_cat, name="update_bgoods_cat"),
    path(r"<int:cid>/delete_bgoods_cat", delete_bgoods_cat, name="delete_bgoods_cat"),
    path(r"b_goods_state", b_goods_state, name="b_goods_state"),
    path(r"create_bgoods_state", create_bgoods_state, name="create_bgoods_state"),
    path(r"<int:sid>/update_bgoods_state", update_bgoods_state, name="update_bgoods_state"),
    path(r"<int:sid>/delete_bgoods_state", delete_bgoods_state, name="delete_bgoods_state"),

    # 订单模块
    path(r"b_order_list", b_order_list, name="b_order_list"),
    path(r"<int:oid>/b_order_detail", b_order_detail, name="b_order_detail"),
    path(r"<int:oid>/order_adjust", order_adjust, name="order_adjust"),

    # 论坛模块
    path(r"b_forum_cat", b_forum_cat, name="b_forum_cat"),
    path(r"create_bforum_cat", create_bforum_cat, name="create_bforum_cat"),
    path(r"<int:cid>/update_bforum_cat", update_bforum_cat, name="update_bforum_cat"),
    path(r"<int:cid>/delete_bforum_cat", delete_bforum_cat, name="delete_bforum_cat"),
    path(r"b_forum_topic", b_forum_topic, name="b_forum_topic"),
    path(r"create_bforum_topic", create_bforum_topic, name="create_bforum_topic"),
    path(r"<int:tid>/update_bforum_topic", update_bforum_topic, name="update_bforum_topic"),
    path(r"<int:tid>/delete_bforum_topic", delete_bforum_topic, name="delete_bforum_topic"),
    path(r"b_forum_list", b_forum_list, name="b_forum_list"),
    path(r"<int:fid>/b_forum_detail", b_forum_detail, name="b_forum_detail"),
    path(r"<int:fid>/b_forum_comment", b_forum_comment, name="b_forum_comment"),
    path(r"<int:fid>/disable_forum", disable_forum, name="disable_forum"),
    path(r"<int:fid>/enable_forum", enable_forum, name="enable_forum"),

    # 配置中心
    path(r"mct_config_list", mct_config_list, name="mct_config_list"),
    path(r"mct_config_list", mct_config_list, name="mct_config_list"),
    path(r"create_mct_config", create_mct_config, name="create_mct_config"),
    path(r"<int:cid>/update_mct_config", update_mct_config, name="update_mct_config"),

    # 帮助中心
    path(r"bnews_list", bnews_list, name="bnews_list"),
    path(r"create_bnews", create_bnews, name="create_bnews"),
    path(r"<int:nid>/bnews_detail", bnews_detail, name="bnews_detail"),
    path(r"<int:nid>/update_bnews", update_bnews, name="update_bnews"),
    path(r"<int:nid>/delete_news", delete_news, name="delete_news"),
    path(r"bhd_list", bhd_list, name="bhd_list"),
    path(r"<int:top_id>/bhd_detail", bhd_detail, name="bhd_detail"),
    path(r"bhd_reply", bhd_reply, name="bhd_reply"),
    path(r"<int:tid>/bhd_close", bhd_close, name="bhd_close"),

    # 登陆
    path(r"b_login", b_login, name="b_login"),
    path(r"b_logout", b_logout, name="b_logout"),
]