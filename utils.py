def getById(model, _id, session):
    """
    общий метод получения сущности по id в базе
    :param model: модель сущности бд
    :param _id: id сущности в базе
    :param session: сессия пула подключений к базе
    :return: сущность или raise Exception
    """

    try:
        entity = session.query(model) \
            .filter(model.id == _id) \
            .one()
        return entity

    except Exception:
        session.rollback()
        raise
