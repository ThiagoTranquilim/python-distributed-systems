class GreetingService:
    def handle(self, request):
        name = request.payload.get("name")

        if not name:
            raise ValueError("Name não pode ser vazio.")

        return {
            "message": f"Olá, {name}!"
        }