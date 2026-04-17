"""Affichage et formatage des résultats de benchmark."""

from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

class BenchmarkFormatter:
    """Formatte les résultats de benchmark pour l'affichage."""

    def __init__(self):
        self.console = Console()

    def format_table(self, metrics: Dict[str, Any]) -> str:
        """Produit un tableau formaté des métriques."""
        table = Table(title="Model Benchmark Results")
        table.add_column("Model", justify="left", style="cyan", no_wrap=True)
        table.add_column("Latency (s)", justify="right", style="green")
        table.add_column("Tokens", justify="right", style="magenta")
        table.add_column("Score", justify="right", style="yellow")

        for model, data in metrics["models"].items():
            table.add_row(
                model,
                f"{data.get('latency', 0):.2f}",
                str(data.get("tokens", 0)),
                f"{data.get('score', 0):.1f}"
            )

        return table

    def show_winner(self, metrics: Dict[str, Any]):
        """Identifie et affiche le meilleur modèle."""
        best_model = None
        best_score = -1

        for model, data in metrics["models"].items():
            score = data.get("score", 0.0)
            if score > best_score:
                best_score = score
                best_model = model

        if best_model:
            self.console.print(f"\n[bold green]Winner: {best_model}[/bold green] with score {best_score:.1f}")

    def show_comparison(self, metrics: Dict[str, Any]):
        """Affiche le tableau et le gagnant."""
        self.console.print(self.format_table(metrics))
        self.show_winner(metrics)

# Exemple d'utilisation
# formatter = BenchmarkFormatter()
# formatter.show_comparison(metrics)