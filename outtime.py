def main():
    db = input()
    global_init(db)
    session = create_session()
    o = {}
    for user in session.query(User):
        o[user.id] = user.name + ' ' + user.surname
    for job in session.query(Jobs).filter(Jobs.address == 'module_1' or Jobs.age < 21):
        user.address == 'module_3'
    session.commit()


if __name__ == '__main__':
    main()
