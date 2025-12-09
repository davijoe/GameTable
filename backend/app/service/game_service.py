from app.repository.game.game_repository_factory import get_game_repository
from app.schema.artist_schema import ArtistRead
from app.schema.designer_schema import DesignerRead
from app.schema.game_schema import GameCreate, GameDetail, GameRead, GameUpdate
from app.schema.mechanic_schema import MechanicRead
from app.schema.publisher_schema import PublisherRead


class GameService:
    def __init__(self):
        self.repo = get_game_repository()

    def list(self, offset, limit, search, sort_by):
        rows, total = self.repo.list(offset, limit, search, sort_by)

        for r in rows:
            r.bgg_rating = round(r.bgg_rating, 2) # round because of validator

            #clean data before validation
            if r.year_published < 1901:
                r.year_published = 1901
            if r.min_players < 1:
                r.min_players = 1
            if r.max_players < 1:
                r.max_players = 1

        return [GameRead.model_validate(r) for r in rows], total

    def get(self, game_id):
        obj = self.repo.get(game_id)
        obj.bgg_rating = round(obj.bgg_rating, 2) # round because of validator
        return GameRead.model_validate(obj) if obj else None

    def get_detail(self, game_id):
        obj = self.repo.get_detail(game_id)
        if not obj:
            return None

        return GameDetail.model_validate({
            **obj.__dict__,
            "artists": [ArtistRead.model_validate(a) for a in obj.artists],
            "designers": [DesignerRead.model_validate(d) for d in obj.designers],
            "publishers": [PublisherRead.model_validate(p) for p in obj.publishers],
            "mechanics": [MechanicRead.model_validate(m) for m in obj.mechanics],
        })

    def create(self, payload: GameCreate):
        return GameRead.model_validate(self.repo.create(payload.model_dump()))

    def update(self, game_id, payload: GameUpdate):
        obj = self.repo.update(game_id, payload.model_dump(exclude_unset=True))
        return GameRead.model_validate(obj) if obj else None

    def delete(self, game_id):
        return self.repo.delete(game_id)

