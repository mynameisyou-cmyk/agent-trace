import uuid

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text

from agent_trace.db import auth_session

security = HTTPBearer()


async def get_project_id(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> uuid.UUID:
    """Validate an at_ prefixed API key against agent_tools.apiKeys table.

    Returns the project_id associated with the key.
    """
    token = credentials.credentials
    if not token.startswith("at_"):
        raise HTTPException(status_code=401, detail="Invalid API key format")

    async with auth_session() as db:
        # agent_tools stores keys as plaintext with at_ prefix in apiKeys table
        result = await db.execute(
            text('SELECT "projectId" FROM "apiKeys" WHERE key = :key'),
            {"key": token},
        )
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return row[0]
