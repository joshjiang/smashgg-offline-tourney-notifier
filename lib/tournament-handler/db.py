class TournamentsTable(object):
    def __init__(self, table_resource):
        self._table = table_resource

    def insert_tournament(self, id):
        """Insert a tournament into the table."""
        # Return an error if we don't have tournament_id in the JSON event
        if not id:
            return Exception("Invalid event. Must include key 'tournament_id'")
        try:
            self._table.put_item(
                Item={
                    'tournament_id': id,
                }
            )
        except Exception as e:
            print(e)
            return e

    def get_tournament(self, id: int):
        """Get a tournament from the table."""
        # Return an error if we don't have tournament_id in the JSON event
        if not id:
            print("Invalid id. Must include id")
            return Exception("Invalid id. Must include id")
        try:
            item = self._table.get_item(
                TableName='tournament-table',
                Key={"tournament_id": id}
            )
            if item.get('Item', None):
                return item
            return None
        except Exception as e:
            print(e)
            return e
