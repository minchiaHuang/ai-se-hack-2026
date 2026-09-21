"""Set up the phone interview once: an ElevenLabs agent and the team's Twilio number.

    ELEVENLABS_API_KEY=... TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=... \\
        TWILIO_PHONE_NUMBER=+61... python3 -m skeleton.tools.phone_agent
    python3 -m skeleton.tools.phone_agent --call +61400000000

The first form creates the agent and imports the number, then prints the two
IDs to put in the environment. An ID already set is kept, so running it again
creates nothing twice; unset ELEVENLABS_AGENT_ID to make a new agent after the
prompt changes. --call rings a phone with those IDs, to test the whole chain
before the page uses it. Standard library only, keys from the environment only.
"""
import os
import sys

from skeleton.core import phone

NEEDED = ("ELEVENLABS_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER")


def main(argv=(), post=None):
    """Exit status, never a traceback: this is run by hand."""
    if "--call" in argv:
        number = argv[argv.index("--call") + 1] if len(argv) > argv.index("--call") + 1 else ""
        body = phone.start_call(number)
        if "conversation_id" not in body:
            print(body.get("reason", "The call was not placed."), file=sys.stderr)
            return 1
        print(f"Calling {number}. conversation_id={body['conversation_id']}")
        return 0
    env = {name: os.environ.get(name, "") for name in NEEDED}
    missing = [name for name, value in env.items() if not value]
    if missing:
        print("Set " + ", ".join(missing) + " first.\n" + __doc__, file=sys.stderr)
        return 2
    key = env["ELEVENLABS_API_KEY"]
    agent_id = os.environ.get("ELEVENLABS_AGENT_ID", "")
    number_id = os.environ.get("ELEVENLABS_PHONE_NUMBER_ID", "")
    try:
        if not agent_id:
            agent_id = phone.create_agent(key, post=post)
        if not number_id:
            number_id = phone.import_number(key, env["TWILIO_PHONE_NUMBER"],
                                            env["TWILIO_ACCOUNT_SID"], env["TWILIO_AUTH_TOKEN"],
                                            post=post)
    except Exception as error:
        # The service's reason, never the request: the request carries the Twilio token.
        print(f"{phone._failure(error, 'Setup')['reason']} ({type(error).__name__}) "
              "Check the keys and the number, then run again.", file=sys.stderr)
        return 1
    print("Add these to your environment:")
    print(f"ELEVENLABS_AGENT_ID={agent_id}")
    print(f"ELEVENLABS_PHONE_NUMBER_ID={number_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv[1:]))
