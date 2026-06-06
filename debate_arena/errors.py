class DebateArenaError(Exception):
    """Base error for Debate Arena failures."""


class ConfigError(DebateArenaError):
    """Raised when runtime configuration is incomplete or invalid."""


class LoaderError(DebateArenaError):
    """Raised when an input Skill cannot be loaded."""


class LLMConfigurationError(DebateArenaError):
    """Raised when the requested LLM provider is not configured."""


class LLMRuntimeError(DebateArenaError):
    """Raised when an LLM call fails."""


class InvalidLLMOutput(DebateArenaError):
    """Raised when an LLM response cannot be parsed or validated."""
