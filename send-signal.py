from rich.console import Console
from rich.logging import RichHandler
import logging
import config
import requests

# Set up rich logging
logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

console = Console()

def send_signal(pair, long_or_short, simulate=False):
    """
    Send or simulate sending a signal to ProfitTrailer.
    """
    label = config.LONG_SIGNAL_LABEL if long_or_short == 'L' else config.SHORT_SIGNAL_LABEL
    message = (
        f"token={config.SIGNAL_TOKEN}\n"
        "position=OPEN\n"
        f"pair={pair}\n"
        "valid=60s\n"
        f"label={label}\n"
        "mode=STRATEGY"
    )
    
    if simulate:
        formatted_message = message.replace('\n', ', ')
        logger.info(f"Simulated Signal: {formatted_message}")
        return "Simulated"

    url = "https://signal.profittrailer.com/api/tradingview/process"
    formatted_message = message.replace('\n', ', ')
    logger.info(f"Sending POST request to {url} with body: {formatted_message}")
    response = requests.post(url, data=message, headers={'Content-Type': 'text/plain'})

    # Logging detailed response information
    logger.info("Response Details:")
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response Headers: {response.headers}")
    logger.info(f"Response Body: {response.text}")
    if 'json' in response.headers.get('Content-Type', ''):
        try:
            logger.info(f"Response JSON: {response.json()}")
        except ValueError:
            logger.info("No JSON response content.")
    else:
        logger.info("No JSON in response.")
    return response.text


def main():
    pair = input("Enter the PAIR: ").strip()
    if not pair.endswith("USDT"):
        pair += "USDT"

    long_or_short = input("Long or Short? (L/S): ").strip().upper()
    if long_or_short not in ['L', 'S']:
        logger.error("Invalid option. Please enter 'L' for Long or 'S' for Short.")
        return

    simulate_option = input("Send or Sim the signal? (Send/Sim): ").strip().lower()
    send = simulate_option == "send"

    logger.info(f"{'Simulating' if not send else 'Sending'} signal for {pair} as {'Long' if long_or_short == 'L' else 'Short'}")
    response = send_signal(pair, long_or_short, not send)
    logger.info(f"{'Simulated' if not send else 'Sent'}. Response: {response}")

if __name__ == "__main__":
    main()
