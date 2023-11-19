import dns.message
import dns.rcode
import dns.rdatatype
import dns.query
import dns.resolver
import yaml

def load_config():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config

def handle_query(query):
    try:
        config = load_config()

        # Загрузка DNS-запроса
        dns_query = dns.message.from_wire(query)

        for question in dns_query.question:
            qtype = dns.rdatatype.to_text(question.rdtype)
            qname = dns.name.to_text(question.name)

            # Проверка находится ли DNS-запрос в доменах WebRTC
            if 'stun' in qname or 'turn' in qname:
                print(f'Rewriting WebRTC IP for {qname}...')

                # Создание и отправка DNS-запроса к выбранному резолверу
                resolver = dns.resolver.Resolver(configure=False)
                resolver.nameservers = [config['resolver']['address']]
                resolver.port = config['resolver']['port']

                response = resolver.resolve(qname, qtype)

                # Замена IP-адреса WebRTC на целевой IP
                response.answer[0].items[0].address = config['webRTC']['targetIP']

                # Устанавливаем код успешного ответа (NOERROR)
                response.set_rcode(dns.rcode.NOERROR)

                # Возвращаем модифицированный DNS-ответ
                return response.to_wire()

        # Передача DNS-запроса непосредственно к выбранному резолверу
        dns_resolver = dns.resolver.Resolver(configure=False)
        dns_resolver.nameservers = [config['resolver']['address']]
        dns_resolver.port = config['resolver']['port']
        dns_response = dns_resolver.query(dns_query.question[0].name, dns_query.question[0].rdtype)

        # Возвращаем DNS-ответ как есть
        return dns_response.to_wire()
    except Exception as e:
        # Обработка возможных ошибок
        print(f'Error: {e}')
        return b''

def main():
    # Запуск DNS-прокси
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['127.0.0.1']
    dns.resolver.default_resolver.port = 5353

    dns.resolver.get_default_resolver().cache.clear()

    try:
        udp_server = dns.server.DatagramDNSHandler(
            handle_query,
            dns.message.Message,
            dns.message.Message,
        )
        udp_server.run()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()