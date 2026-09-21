"""Direction 7 - spoken, undocumented work history into Australian structures.

The constrained task is extraction and mapping. Not generation: nothing is
claimed that the person did not say. Not scoring: no number is put on a human.

The red lines are enforced here, before the model is called, because the data
belongs to people whose safety can depend on it not existing anywhere.
"""
from skeleton.core import registry

KEY = "d7"
NAME = "Undocumented experience"
METRIC = "evidence items mapped to a transcript line"

# Only the languages we can stand behind. Mandarin is what the team records
# and checks word for word; Arabic is configured but not validated by a native
# speaker, so nothing claims it works well. Farsi and Swahili are left out
# because nobody here can verify them; Dari, Tigrinya, Rohingya and Hazaragi
# have no ElevenLabs voice at all. We refuse rather than silently use English.
SUPPORTED_LANGUAGES = ("zh", "ar")

# A resume the person brings is read, not heard, so English is added: the team
# can read it word for word, and a partial record such as an overseas resume
# is often in English. Spoken input keeps SUPPORTED_LANGUAGES unchanged.
WRITTEN_LANGUAGES = ("en", "zh", "ar")

# The interview is the primary path, so a payload without a source is one.
RESUME = "resume"
RESUME_METRIC = "evidence items mapped to a resume line"

# Fields that identify a refugee, or expose a protection claim. A database row
# holding these is a route back to the people they fled.
FORBIDDEN_FIELDS = (
    "country_of_origin",
    "visa_status",
    "protection_claim",
    "biometric",
)

# Scoring a job's fit is allowed. Scoring the person is not.
PERSON_SCORE_FIELDS = ("candidate_score", "employability_score", "person_rating")


class RedLineError(Exception):
    """Raised when input would cross an ethical red line."""


class UnsupportedLanguageError(Exception):
    """Raised rather than falling back to English behind the user's back."""


def guard(payload):
    for field in payload:
        lowered = field.lower()
        if any(marker in lowered for marker in FORBIDDEN_FIELDS):
            raise RedLineError(
                f"{field}: identifying or protection-related field must never be collected"
            )
        if lowered in PERSON_SCORE_FIELDS:
            raise RedLineError(f"{field}: this system does not score people")

    if not payload.get("consent"):
        raise RedLineError("consent was not given; nothing may be processed")

    language = payload.get("language")
    if payload.get("source") == RESUME:
        if language not in WRITTEN_LANGUAGES:
            raise UnsupportedLanguageError(
                f"{language}: not supported for a written resume. This demo reads "
                "resumes in English (en) and Mandarin (zh), and Arabic (ar) is "
                "configured but not yet validated by a native speaker. We will "
                "not fake a language we cannot verify."
            )
        return
    if language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageError(
            f"{language}: not supported. This demo runs in Mandarin (zh), and "
            "Arabic (ar) is configured but not yet validated by a native "
            "speaker. We will not fake a language we cannot verify."
        )


def prepare(payload):
    """What the model sees: the transcript, or the numbered resume lines, and
    the occupational frame, nothing else."""
    occupation_key = payload["occupation"]
    # Kept under its own key so the live model cites resume lines as resume
    # lines, never as transcript timestamps the person did not speak at.
    lines_key = RESUME if payload.get("source") == RESUME else "transcript"
    anzsco, osca = registry.classifications(occupation_key)
    qualification = registry.occupation(occupation_key)["qualification"]
    return {
        lines_key: payload[lines_key],
        "candidate_units": registry.all_units(occupation_key),
        "anzsco": anzsco,
        "osca": osca,
        # Code and title only: without it the live model has no qualification
        # to cite, and live._allowed_codes() drops every qualification it names.
        "qualification": {"code": qualification["code"], "title": qualification["title"]},
    }


def target_fields(payload):
    """What the model is asked for. The gate is not here: it is reference data
    about the occupation, looked up, never guessed."""
    return ("anzsco_code", "osca_code", "qualification", "units_evidenced")


def metric(accepted, payload):
    """Evidence items that carry a transcript locator. Nothing else counts."""
    return sum(1 for s in accepted if s.sources)
