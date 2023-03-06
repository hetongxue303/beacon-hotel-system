import datetime

from utils.order import get_uuid

user_data = [
    {
        'username': 'admin',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '管理员', 'gender': '1', 'is_admin': '1', 'is_status': '1'
    },
    {
        'username': 'test',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '测试员工', 'gender': '2', 'is_admin': '0', 'is_status': '1'
    }
]

role_data = [
    {'role_name': '管理员', 'is_status': '1', 'description': '拥有所有权限'},
    {'role_name': '酒店员工', 'is_status': '1', 'description': '员工权限'}
]

menu_data = [
    {
        'parent_id': 0, 'menu_title': '首页', 'menu_type': '1', 'router_name': 'dashboard', 'sub_count': 0,
        'router_path': '/dashboard', 'component': 'dashboard/index.vue', 'sort': 1, 'icon': 'index',
        'permission': '*', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 0, 'menu_title': '房间类型', 'menu_type': '1', 'router_name': 'type',
        'router_path': '/type', 'component': 'type/index.vue', 'sort': 2, 'icon': 'index', 'sub_count': 0,
        'permission': 'type:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 0, 'menu_title': '房间管理', 'menu_type': '1', 'router_name': 'room',
        'router_path': '/room', 'component': 'room/index.vue', 'sort': 3, 'icon': 'index', 'sub_count': 0,
        'permission': 'room:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 0, 'menu_title': '客户管理', 'menu_type': '1', 'router_name': 'customer',
        'router_path': '/customer', 'component': 'customer/index.vue', 'sort': 4, 'icon': 'index', 'sub_count': 0,
        'permission': 'customer:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 0, 'menu_title': '订单管理', 'menu_type': '1', 'router_name': 'order',
        'router_path': '/order', 'component': '', 'sort': 5, 'icon': 'index', 'sub_count': 3,
        'permission': '', 'is_show': '1', 'is_sub': '1', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 5, 'menu_title': '预约订单', 'menu_type': '2', 'router_name': 'reservation', 'sub_count': 0,
        'router_path': '/order/reservation', 'component': 'order/reservation/index.vue', 'sort': 6, 'icon': 'index',
        'permission': 'order:reservation:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 5, 'menu_title': '入住订单', 'menu_type': '2', 'router_name': 'stay', 'sub_count': 0,
        'router_path': '/order/stay', 'component': 'order/stay/index.vue', 'sort': 7, 'icon': 'index',
        'permission': 'order:stay:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 5, 'menu_title': '所有订单', 'menu_type': '2', 'router_name': 'all', 'sub_count': 0,
        'router_path': '/order/all', 'component': 'order/all/index.vue', 'sort': 8, 'icon': 'index',
        'permission': 'order:all:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 0, 'menu_title': '系统管理', 'menu_type': '1', 'router_name': 'system',
        'router_path': '/system', 'component': '', 'sort': 9, 'icon': 'system', 'sub_count': 3,
        'permission': '', 'is_show': '1', 'is_sub': '1', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 9, 'menu_title': '员工管理', 'menu_type': '2', 'router_name': 'user', 'sub_count': 0,
        'router_path': '/system/user', 'component': 'system/user/index.vue', 'sort': 10, 'icon': 'system',
        'permission': 'system:user:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 9, 'menu_title': '角色管理', 'menu_type': '2', 'router_name': 'role', 'sub_count': 0,
        'router_path': '/system/role', 'component': 'system/role/index.vue', 'sort': 11, 'icon': 'role',
        'permission': 'system:role:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 9, 'menu_title': '菜单管理', 'menu_type': '2', 'router_name': 'menu', 'sub_count': 0,
        'router_path': '/system/menu', 'component': 'system/menu/index.vue', 'sort': 12, 'icon': 'menu',
        'permission': 'system:menu:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    },
    {
        'parent_id': 0, 'menu_title': '关于酒店', 'menu_type': '1', 'router_name': 'about',
        'router_path': '/about', 'component': 'about/index.vue', 'sort': 13, 'icon': 'about', 'sub_count': 0,
        'permission': 'system:menu:list', 'is_show': '1', 'is_sub': '0', 'is_delete': '0', 'description': '无'
    }
]

user_role_data = [
    {'user_id': 1, 'role_id': 1},
    {'user_id': 2, 'role_id': 2}
]

role_menu_data = [
    {'role_id': 1, 'menu_id': 1},
    {'role_id': 1, 'menu_id': 2},
    {'role_id': 1, 'menu_id': 3},
    {'role_id': 1, 'menu_id': 4},
    {'role_id': 1, 'menu_id': 5},
    {'role_id': 1, 'menu_id': 6},
    {'role_id': 1, 'menu_id': 7},
    {'role_id': 1, 'menu_id': 8},
    {'role_id': 1, 'menu_id': 9},
    {'role_id': 1, 'menu_id': 10},
    {'role_id': 1, 'menu_id': 11},
    {'role_id': 1, 'menu_id': 12},
    {'role_id': 1, 'menu_id': 13},
    {'role_id': 2, 'menu_id': 1},
    {'role_id': 2, 'menu_id': 13}
]

room_type_data = [
    {'room_type_name': '大床房', 'description': '这是一间大床房！'},
    {'room_type_name': '小床房', 'description': '这是一间小床房！'},
    {'room_type_name': '单人房', 'description': '这是一间单人房！'},
    {'room_type_name': '双人房', 'description': '这是一间双人房！'},
    {'room_type_name': '套房', 'description': '这是一间标准套房！'}
]

room_data = [
    {'room_name': '豪华小床房', 'room_type_id': 2, 'room_price': 599.99, 'room_bed': 1, 'is_state': '1',
     'room_count': 2, 'is_status': '1', 'room_detail': '豪华小床房，适合1-2人居住！'},
    {'room_name': '豪华双人房', 'room_type_id': 4, 'room_price': 800.00, 'room_bed': 1, 'is_state': '1',
     'room_count': 4, 'is_status': '1', 'room_detail': '豪华双人房，适合2-4人居住！'},
    {'room_name': '豪华套房', 'room_type_id': 5, 'room_price': 999.99, 'room_bed': 2, 'is_state': '0',
     'room_count': 4, 'is_status': '1', 'room_detail': '豪华套房，适合4-6人居住！'},
]

customer_data = [
    {
        'customer_name': '周利华', 'customer_account': 'user1', 'id_card': '500112200205015689',
        'customer_password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py', 'telephone': '15447889586'
    },
    {
        'customer_name': '刘忠鑫', 'customer_account': 'user2', 'id_card': '500112200204215689',
        'customer_password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py', 'telephone': '15447759686'
    },
    {
        'customer_name': '李立峰', 'customer_account': 'user3', 'id_card': '500112200101195899',
        'customer_password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py', 'telephone': '15687889586'
    }
]

order_data = [
    {
        'order_num': get_uuid(), 'customer_id': 1, 'room_id': 2, 'is_handler': '1', 'count_num': 2,
        'start_date_time': datetime.datetime(2023, 2, 25, 9, 00, 00),
        'leave_date_time': datetime.datetime(2023, 2, 28, 9, 00, 00),
        'description': '无'
    },
    {
        'order_num': get_uuid(), 'customer_id': 3, 'room_id': 1, 'is_handler': '1', 'count_num': 1,
        'start_date_time': datetime.datetime(2023, 2, 26, 18, 00, 00),
        'leave_date_time': datetime.datetime(2023, 3, 2, 18, 00, 00),
        'description': '测试北备注'
    }
]
