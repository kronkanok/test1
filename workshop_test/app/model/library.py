from typing import Optional, List
from pydantic import BaseModel, Field


class createLibraryModel(BaseModel):
    name: str
    picture_url: str
    id: str = Field(min_length=1, max_length=10)
    price: str
    stories: List[str]
    Numberofpages: int
    Volumeimagesize: int
    Papertexture: str
    Papertype: str
    publisher: str
    MouthyearofPublication: int


class updateLibraryModel(BaseModel):

    name: Optional[str]
    picture_url: Optional[str]
    price: Optional[int]
    stories: Optional[List[str]]
    Numberofpages: Optional[int]
    Volumeimagesize: Optional[int]
    Papertexture: Optional[str]
    Papertype: Optional[str]
    publisher: Optional[str]
    MouthyearofPublication: Optional[int]
