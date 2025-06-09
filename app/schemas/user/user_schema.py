from datetime import datetime

# from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

#from app.models.user.user_model import AccountType, UserStatus, UserType


# class EducationSchema(BaseModel):
#     degree: str
#     institution: str
#     year: int


# class ExperienceSchema(BaseModel):
#     title: str
#     company: str
#     duration: str
#     summary: str


# class ReviewSchema(BaseModel):
#     reviewer: str
#     text: str
#     sentiment: Optional[str] = None


# class UserCreate(BaseModel):
#     """Schema for creating a new user"""

#     walletAddress: str
#     email: Optional[EmailStr] = None
#     username: str
#     profileImage: Optional[HttpUrl] = None
#     bio: Optional[str] = None
#     skills: List[str] = []
#     portfolioLinks: List[str] = []
#     education: List[EducationSchema] = []
#     certifications: List[str] = []
#     experience: List[ExperienceSchema] = []
#     accountType: AccountType = AccountType.USER
#     userType: UserType = UserType.STUDENT
#     status: UserStatus = UserStatus.ACTIVE
#     kycVerified: bool = False
#     verificationLevel: int = Field(0, ge=0, le=5)
#     isBlacklisted: bool = False


# class UserUpdate(BaseModel):
#     """Schema for updating user fields"""

#     email: Optional[EmailStr] = None
#     username: Optional[str] = None
#     profileImage: Optional[HttpUrl] = None
#     bio: Optional[str] = None
#     skills: Optional[List[str]] = None
#     portfolioLinks: Optional[List[str]] = None
#     education: Optional[List[EducationSchema]] = None
#     experience: Optional[List[ExperienceSchema]] = None
#     status: Optional[UserStatus] = None
#     certifications: Optional[List[str]] = None
#     verificationLevel: Optional[int] = Field(None, ge=0, le=5)


# class UserResponse(BaseModel):
#     """Schema for user response"""

#     id: str
#     walletAddress: str
#     email: Optional[EmailStr] = None
#     username: str
#     profileImage: Optional[HttpUrl] = None
#     bio: Optional[str] = None
#     skills: List[str] = []
#     portfolioLinks: List[str] = []
#     education: List[EducationSchema] = []
#     certifications: List[str] = []
#     experience: List[ExperienceSchema] = []
#     accountType: AccountType
#     userType: UserType
#     status: UserStatus
#     kycVerified: bool
#     verificationLevel: int
#     isBlacklisted: bool
#     trustScore: Optional[float] = None
#     reputationScore: Optional[float] = None
#     totalEarnings: float
#     completedProjects: int
#     openProjects: int
#     reviewsCount: int
#     averageRating: Optional[float] = None
#     reviews: List[ReviewSchema] = []
#     disputeCount: int
#     conversationHistoryId: Optional[str] = None
#     projectComplexityRating: Optional[float] = None
#     createdAt: datetime
#     updatedAt: datetime

#     class Config:
#         from_attributes = True

# ------------------ Input Schema for Matching ---------------

class ProjectInput(BaseModel):
    clientId: str
    projectId: str
    description: str
    projecttype: list[str]
    skills: list[str]
    budget: int
    timeline: int

class FreelancerInput(BaseModel):
    flancerId: str
    skills: list[str]
    favouriteProject: str
    rating: int
    experince: int
    bid: int
    exp_timeline: int
    proposal: str

class MatchRequest(BaseModel):
    project: ProjectInput
    freelancers: list[FreelancerInput] 