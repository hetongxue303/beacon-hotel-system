user_data = [
    {
        'username': 'admin',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '管理员', 'gender': '1', 'is_admin': '1', 'is_status': '1'
    },
    {
        'username': 'test',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '测试员工', 'gender': '2', 'is_admin': '0', 'is_status': '0'
    }
]

role_data = [
    {'role_name': '管理员', 'is_status': '1', 'description': '拥有所有权限'},
    {'role_name': '员工', 'is_status': '1', 'description': '员工权限'}
]

menu_data = []

user_role_data = [
    {'user_id': 1, 'role_id': 1},
    {'user_id': 2, 'role_id': 2}
]

role_menu_data = []

room_type_data = [
    {'room_type_name': '大床房', 'description': '这是一间大床房！'},
    {'room_type_name': '小床房', 'description': '这是一间小床房！'},
    {'room_type_name': '单人房', 'description': '这是一间单人房！'},
    {'room_type_name': '双人房', 'description': '这是一间双人房！'},
    {'room_type_name': '套房', 'description': '这是一间标准套房！'}
]

room_data = [
    {'room_name': '豪华小床房', 'room_type_id': 2, 'room_price': 599.99, 'room_bed': 1,
     'room_count': 2, 'is_status': '1', 'room_detail': '豪华小床房，适合1-2人居住！'},
    {'room_name': '豪华双人房', 'room_type_id': 4, 'room_price': 800.00, 'room_bed': 1,
     'room_count': 4, 'is_status': '1', 'room_detail': '豪华双人房，适合2-4人居住！'},
    {'room_name': '豪华套房', 'room_type_id': 5, 'room_price': 999.99, 'room_bed': 2,
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

order_data = []
