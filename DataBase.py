import psycopg2
from operator import itemgetter
import jellyfish
from Summary import Summary

class DataBase:

    def __init__(self):
        self.connection = self.create_connection(
            "oqwiuwgq", "oqwiuwgq", "3Wj9NZMWY34rt3JlpHBC2PAvQsC6q2D-", "tai.db.elephantsql.com", "5432"
        )

        self.cursor = self.connection.cursor()

        select_malfunctions = "SELECT * from malfunctions"
        self.malfunctions = self.execute_read_query(self.connection, select_malfunctions)

        select_actions = "SELECT * from actions"
        self.actions = self.execute_read_query(self.connection, select_actions)

        self.malfunctions = self.execute_read_query(self.connection, select_malfunctions)

    def create_connection(self, db_name, db_user, db_password, db_host, db_port):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Подключение к БД прошло успешно")
        except psycopg2.OperationalError as e:
            print(f"The error '{e}' occurred")
        return self.connection

    def close_db(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def execute_read_query(self, connection, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except psycopg2.Error as e:
            print(f"Ошибка '{e}' при чтении из БД")

    def execute_read_query_params(self, connection, query, param):
        try:
            self.cursor.execute(query, (param))
            result = self.cursor.fetchall()
            result = list(map(list, result))
            return result
        except psycopg2.Error as e:
            print(f"Ошибка '{e}' при чтении из БД")

    def find_relevant_info(self, text):
        results = []
        methods = []
        for malfunction in self.malfunctions:
            accuracy = jellyfish.damerau_levenshtein_distance(text, malfunction[1])
            results.append({'id': malfunction[0], 'malfunction': malfunction[1], 'accuracy': accuracy,
                            'action_id': malfunction[2]})

        sort_array = sorted(results, key=itemgetter('accuracy'))
        # print(sort_array[-1])
        some_id = sort_array[0]['id']
        select_reasons = "SELECT * FROM reasons WHERE malfunction_id = %s;"
        reasons = self.execute_read_query_params(self.connection, select_reasons, [some_id])
        # print('Причины:')
        # print(reasons)
        
        summary_tokenizer = Summary()
        for reason in reasons:
            reason_id = reason[0]
            select_methods = "SELECT * FROM methods WHERE reason_id = %s;"
            method = self.execute_read_query_params(self.connection, select_methods, [reason_id])

            method[0][1] = summary_tokenizer.tokenize_summary(method[0][1])

            methods.append(method)

            # print('Метод:')
            # print(method)

        reasons_and_methods = '\n'.join(
            [f'{r + 1}) {reasons[r][1]} ({methods[r][0][1]})' for r in range(len(reasons))])
        

        result_text = f"Неисправность:\n\n{sort_array[-1]['malfunction']}\n\nВероятные причины / Способы устранения:\n\n" \
                      f"{reasons_and_methods}"
        return result_text


if __name__ == "__main__":
    # a = DataBase()
    # print(a.find_relevant_info("Рейки топливных насосов не выдвигаются на подачу топлива или выходят медленно"))
    # print(a.find_relevant_info("Рейки топливных насосов не  на подачу топлива или выходят "))
    text1 = 'При нажатии кнопки "Пуск дизеля" контактор КМН включается, но маслопрокачивающий насос не работает'
    text2 = 'При нажатии кнопки "Пуск дизеля" маслопрокачивающий насос не работает'
    text3 = 'при нажатиикнопка пуск дизеля контакторкмн включается маслопрокачивающий насос не работает'

    text4 = 'не включилось ру6'
    text5 = 'рушесть не работает'
    text6 = 'ктн не включаются'

    text7 = "при повышении температуры воды и масла частота вращения вала вентилятора холодильника увеличивается, жалюзи не открываются."

    print(jellyfish.levenshtein_distance(text1, text2))
    print(jellyfish.levenshtein_distance(text1, text3))
    print(jellyfish.levenshtein_distance(text1, text7))
    print("damerau_levenshtein_distance")
    print(jellyfish.levenshtein_distance(text4, text5))
    print(jellyfish.levenshtein_distance(text4, text6))
    print(jellyfish.levenshtein_distance(text4, text7))