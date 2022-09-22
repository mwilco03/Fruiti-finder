from urllib.parse import unquote
from re import search


class GoogleMapsQueryArgsDeserializer:
    def deserialize(self, query_args: str) -> dict[str, list[str]]:
        return self.decode(list(map(lambda param: unquote(param), query_args.strip('!').split('!'))))

    def decode(self, params: list[str]) -> dict[str, list[str]]:
        data: dict[str, list[str]] = {}

        id: str
        length: int
        type: str

        for i in range(0, len(params)):
            matches = search('^(\d+)m(\d+)', params[i])

            if None is not matches:
                id, length = matches[1], int(matches[2])
                data[id] = self.decode(params[i+1:length])
            else:
                matches = search('^(\d+)([fdibesuv])(.*)$', params[i])

                if None is not matches:
                    id, type, value = matches[1], matches[2], matches[3]

                    if 'i' == type or 'e' == type or 'u' == type:
                        data[id] = int(value)
                    elif 'f' == type:
                        data[id] = float(value)
                    elif 'd' == type:
                        data[id] = float(value)
                    elif 'b' == type:
                        data[id] = bool(value)
                    elif 's' == type or 'v' == type:
                        data[id] = str(value)
                else:
                    raise RuntimeError(f'Unknown param format: ${params[i]}')

        return data
