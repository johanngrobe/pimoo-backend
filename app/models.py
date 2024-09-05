from .database import Base
from datetime import datetime, date
from typing import List, Optional, Literal
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, mapped_column, Mapped

class MobilitySubmission(Base):
    __tablename__ = "mobility_submission"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    author: Mapped[str]
    administration_no: Mapped[str]
    administration_date: Mapped[date]
    label: Mapped[str]
    desc: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))

    objectives: Mapped[Optional[List["MobilityResult"]]] = relationship(back_populates="submission", cascade="all, delete-orphan", passive_deletes=True)


# association table for many-to-many relationship between text_blocks and tags
text_block_tag_association = Table(
    'text_block_tag',
    Base.metadata,
    Column('text_block_id', Integer, ForeignKey('text_block.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"))
)

class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]

class TextBlock(Base):
    __tablename__ = "text_block"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]
    tags: Mapped[Optional[List["Tag"]]] = relationship(secondary=text_block_tag_association, cascade="all, delete")


# association table for many-to-many relationship between indicators and tags
indicator_tag_association = Table(
    'indicator_tag',
    Base.metadata,
    Column('indicator_id', Integer, ForeignKey('indicator.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Indicator(Base):
    __tablename__ = "indicator"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    label: Mapped[str]
    tags: Mapped[Optional[List["Tag"]]] = relationship(secondary=indicator_tag_association, cascade="all, delete")

class MainObjective(Base):
    __tablename__ = "main_objective"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    no: Mapped[int]
    label: Mapped[str]
    sub_objectives: Mapped[List["SubObjective"]] = relationship(back_populates="main_objective", cascade="all, delete")

class SubObjective(Base):
    __tablename__ = "sub_objective"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    no: Mapped[int]
    label: Mapped[str]
    main_objective_id: Mapped[int] = mapped_column(ForeignKey("main_objective.id"), nullable=False)
    main_objective: Mapped["MainObjective"] = relationship(back_populates="sub_objectives",cascade="all, delete")


# association table for many-to-many relationship between mobility_results and indicators
mobility_results_indicators_association = Table(
    'mobility_result_indicators',
    Base.metadata,
    Column('indicator_id', Integer, ForeignKey('indicator.id', ondelete="CASCADE")),
    Column('mobility_subresult_id', Integer, ForeignKey('mobility_subresult.id', ondelete="CASCADE"))
)

Spatial_impact_enum = Literal["locally", "districtwide", "citywide"]

class MobilityResult(Base):
    __tablename__ = "mobility_result"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)

    submission_id: Mapped[int] = mapped_column(ForeignKey("mobility_submission.id", ondelete="CASCADE"))
    submission: Mapped["MobilitySubmission"] = relationship(back_populates="objectives")

    main_objective_id: Mapped[int] = mapped_column(ForeignKey("main_objective.id"))
    main_objective: Mapped["MainObjective"] = relationship()
    target: Mapped[bool] = mapped_column(nullable=False, default=False)

    sub_objectives: Mapped[Optional[List["MobilitySubResult"]]] = relationship(back_populates="main_objective", cascade="all, delete")

class MobilitySubResult(Base):
    __tablename__ = "mobility_subresult"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)

    mobility_result_id: Mapped[int] = mapped_column(ForeignKey("mobility_result.id",ondelete="CASCADE"))
    main_objective: Mapped["MobilityResult"] = relationship(back_populates="sub_objectives")

    sub_objective_id: Mapped[int] = mapped_column(ForeignKey("sub_objective.id"))
    sub_objective: Mapped["SubObjective"] = relationship()

    target: Mapped[bool] = mapped_column(nullable=False, default=False)
    impact: Mapped[Optional[int]]
    spatial_impact: Mapped[Optional[Spatial_impact_enum]]
    annotation: Mapped[Optional[str]]
    indicators: Mapped[Optional[List["Indicator"]]] = relationship(secondary=mobility_results_indicators_association, cascade="all, delete", passive_deletes=True)


Impact_enum = Literal["positive", "negative", "no_effect"]
Impact_duration_enum = Literal["short", "medium", "long"]

class ClimateSubmission(Base):
    __tablename__ = "climate_submission"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, unique=True)
    author: Mapped[str]
    administration_no: Mapped[str]
    administration_date: Mapped[date]
    label: Mapped[str]
    impact: Mapped[Impact_enum]
    impact_ghg: Mapped[Optional[int]]
    impact_adaption: Mapped[Optional[int]]
    impact_desc: Mapped[Optional[str]]
    impact_duration: Mapped[Optional[Impact_duration_enum]]
    alternative_desc: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))

