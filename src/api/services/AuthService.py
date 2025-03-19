from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.typing.UserExists import UserExists
from src.api.typing.UserSuccess import UserSuccess
from src.api.repositories.UserRepository import UserRepository
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)

from .UtilityService import UtilityService


@Service()
class AuthService:
    def __init__(self, logger: Logger, utility_service: UtilityService) -> None:
        self.logger = logger
        self.utility_service = utility_service

    async def register(self, req: CreateUserRequest) -> UserExists:
        email = req.email
        password = req.password

        existing_user = await UserRepository.find_by_email(email)
        if existing_user:
            return {"is_exists": True, "user": existing_user}

        hashed_password: str = await self.utility_service.hash_string(password)
        req = req.model_copy(update={"password": hashed_password})

        created_user = await UserRepository.add(req)
        otp = self.utility_service.generate_random_string(length=6, numeric_only=True)
        await UserRepository.update_by_user(created_user, {"otp": otp})

        otp  # Send OTP to user

        user = self.utility_service.sanitize_user_object(created_user)

        return {"is_exists": False, "user": user}

    async def validate_email(self, req: AuthenticateUserOtp) -> bool:
        email = req.email
        otp = req.otp

        user = await UserRepository.find_by_email(email)
        if not user:
            self.logger.error(  # type: ignore
                "Could not validate user as user does not exist",
                email=email,
                otp=otp,
            )
            return False

        # check otp storage to validate sent otp
        email
        otp

        await UserRepository.update_by_user(
            user, {"is_active": True, "is_enabled": True, "is_validated": True}
        )

        return True

    async def login(self, req: AuthenticateUserRequest) -> UserSuccess:
        email = req.email
        password = req.password

        existing_user = await UserRepository.find_by_email(email)
        if not existing_user:
            return {"is_success": False, "message": "Invalid email or password"}

        is_password_check_ok = await self.utility_service.compare_hash(
            password, existing_user.password
        )
        if not is_password_check_ok:
            return {"is_success": False, "message": "Invalid email or password"}

        if not existing_user.is_validated:
            # resend otp
            return {
                "is_success": False,
                "message": "User account not validated. Please check your email for further instructions",
            }

        if not existing_user.is_active:
            return {
                "is_success": False,
                "message": "User account inactive. Please contact support",
            }

        if not existing_user.is_enabled:
            return {
                "is_success": False,
                "message": "User account disabled. Please contact support",
            }

        if existing_user.is_deleted:
            return {
                "is_success": False,
                "message": "User account has been deleted. Please contact support if you want to restore your account",
            }

        user = self.utility_service.sanitize_user_object(existing_user)

        jwt_details = self.utility_service.generate_jwt(user.email, user.id)

        return {"is_success": True, "user": user, "token": jwt_details}
