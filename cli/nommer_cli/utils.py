

def get_objects(data):
    return [get_object(d) for d in data]


def get_object(data):
    return {"id": data["id"], **data["attributes"]}


def get_data(response):
    data = response.json()

    if response.ok and not data.get("errors"):
        return data.get("data", {}).get("data")
    else:
        click.echo(colored(f"Error getting data: {data.get('errors')}", "red"))