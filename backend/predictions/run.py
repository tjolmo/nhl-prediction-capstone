import asyncio
import sys
from dotenv import load_dotenv
from app.database import AsyncSessionLocal
from predictions.train import train_skater_models, train_skater_classifiers, train_goalie_models, train_goalie_classifiers

load_dotenv()

async def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("skater", "goalie", "all"):
        print("Usage:  python -m predictions.run [skater|goalie|all]")
        sys.exit(1)

    player_type = sys.argv[1]

    async with AsyncSessionLocal() as session:
        if player_type == "skater" or player_type == "all":
            print("═" * 60)
            print("  Training XGBoost regression models")
            print("═" * 60)
            results = await train_skater_models(session)
            if results:
                print("\n  Validation MAE summary:")
                for target, mae in results.items():
                    print(f"    {target:>20s}: {mae}")
            print("═" * 60)
            print()
            print("═" * 60)
            print("  Training XGBoost classification models")
            print("═" * 60)
            clf_results = await train_skater_classifiers(session)
            if clf_results:
                print("\n  Validation summary:")
                for target, metrics in clf_results.items():
                    print(f"    {target + '_clf':>20s}: "
                          f"logloss={metrics['logloss']}  "
                          f"AUC={metrics['auc']}  "
                          f"pos_rate={metrics['pos_rate']}")
            print("═" * 60)
        
        if player_type == "goalie" or player_type == "all":
            print("═" * 60)
            print("  Training XGBoost regression models")
            print("═" * 60)
            results = await train_goalie_models(session)
            if results:
                print("\n  Validation MAE summary:")
                for target, mae in results.items():
                    print(f"    {target:>20s}: {mae}")
            print("═" * 60)
            print()
            print("═" * 60)
            print("  Training XGBoost classification models")
            print("═" * 60)
            clf_results = await train_goalie_classifiers(session)
            if clf_results:
                print("\n  Validation summary:")
                for target, metrics in clf_results.items():
                    print(f"    {target + '_clf':>20s}: "
                          f"logloss={metrics['logloss']}  "
                          f"AUC={metrics['auc']}  "
                          f"pos_rate={metrics['pos_rate']}")
            print("═" * 60)

if __name__ == "__main__":
    asyncio.run(main())
