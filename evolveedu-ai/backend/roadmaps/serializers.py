# roadmaps/serializers.py
from rest_framework import serializers
from .models import (
    SkillCategory, Skill, CareerPath, PersonalizedRoadmap,
    RoadmapMilestone, SkillAssessment, LearningResource, UserProgress
)


class SkillCategorySerializer(serializers.ModelSerializer):
    skills_count = serializers.IntegerField(source='skills.count', read_only=True)

    class Meta:
        model = SkillCategory
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    prerequisites_names = serializers.StringRelatedField(source='prerequisites', many=True, read_only=True)

    class Meta:
        model = Skill
        fields = '__all__'


class SkillListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'category_name', 'difficulty_level',
                  'estimated_hours', 'market_demand', 'is_trending']


class CareerPathSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    required_skills_data = SkillListSerializer(source='required_skills', many=True, read_only=True)
    recommended_skills_data = SkillListSerializer(source='recommended_skills', many=True, read_only=True)

    class Meta:
        model = CareerPath
        fields = '__all__'


class CareerPathListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    required_skills_count = serializers.IntegerField(source='required_skills.count', read_only=True)

    class Meta:
        model = CareerPath
        fields = ['id', 'title', 'description', 'category_name', 'average_salary_min',
                  'average_salary_max', 'job_growth_rate', 'total_estimated_months',
                  'difficulty_level', 'is_popular', 'required_skills_count']


class RoadmapMilestoneSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category.name', read_only=True)

    class Meta:
        model = RoadmapMilestone
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class RoadmapMilestoneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapMilestone
        exclude = ['roadmap', 'created_at', 'updated_at']


class PersonalizedRoadmapSerializer(serializers.ModelSerializer):
    milestones = RoadmapMilestoneSerializer(many=True, read_only=True)
    target_career_path_title = serializers.CharField(source='target_career_path.title', read_only=True)
    target_skills_data = SkillListSerializer(source='target_skills', many=True, read_only=True)

    class Meta:
        model = PersonalizedRoadmap
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'overall_progress_percentage']


class PersonalizedRoadmapListSerializer(serializers.ModelSerializer):
    target_career_path_title = serializers.CharField(source='target_career_path.title', read_only=True)
    milestones_count = serializers.IntegerField(source='milestones.count', read_only=True)
    completed_milestones_count = serializers.SerializerMethodField()

    class Meta:
        model = PersonalizedRoadmap
        fields = ['id', 'title', 'description', 'target_career_path_title',
                  'status', 'overall_progress_percentage', 'start_date',
                  'target_completion_date', 'milestones_count', 'completed_milestones_count',
                  'created_at']

    def get_completed_milestones_count(self, obj):
        return obj.milestones.filter(status='completed').count()


class PersonalizedRoadmapCreateSerializer(serializers.ModelSerializer):
    milestones_data = serializers.ListField(child=RoadmapMilestoneCreateSerializer(), write_only=True, required=False)

    class Meta:
        model = PersonalizedRoadmap
        exclude = ['user', 'created_at', 'updated_at', 'overall_progress_percentage', 'completed_milestones']

    def create(self, validated_data):
        milestones_data = validated_data.pop('milestones_data', [])
        roadmap = PersonalizedRoadmap.objects.create(**validated_data)

        for i, milestone_data in enumerate(milestones_data):
            milestone_data['order'] = i + 1
            RoadmapMilestone.objects.create(roadmap=roadmap, **milestone_data)

        return roadmap


class SkillAssessmentSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category.name', read_only=True)

    class Meta:
        model = SkillAssessment
        fields = '__all__'
        read_only_fields = ['user', 'assessment_date']


class SkillAssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillAssessment
        exclude = ['user', 'assessment_date', 'skill_gaps', 'improvement_suggestions', 'next_learning_steps']


class LearningResourceSerializer(serializers.ModelSerializer):
    skills_data = SkillListSerializer(source='skills', many=True, read_only=True)
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = LearningResource
        fields = '__all__'

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = UserProgress.objects.filter(user=request.user, resource=obj).first()
            if progress:
                return {
                    'status': progress.status,
                    'progress_percentage': progress.progress_percentage,
                    'time_spent_minutes': progress.time_spent_minutes
                }
        return None


class UserProgressSerializer(serializers.ModelSerializer):
    resource_title = serializers.CharField(source='resource.title', read_only=True)
    resource_type = serializers.CharField(source='resource.resource_type', read_only=True)
    roadmap_title = serializers.CharField(source='roadmap.title', read_only=True)

    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ['user', 'last_accessed']


class GenerateRoadmapRequestSerializer(serializers.Serializer):
    career_goal = serializers.CharField(max_length=200)
    current_skills = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    experience_level = serializers.ChoiceField(choices=Skill.DIFFICULTY_LEVELS, default='beginner')
    time_commitment_hours_per_week = serializers.IntegerField(min_value=1, max_value=80, default=10)
    target_months = serializers.IntegerField(min_value=1, max_value=60, default=12)
    preferred_learning_style = serializers.ChoiceField(
        choices=[
            ('visual', 'Visual'),
            ('hands_on', 'Hands-on'),
            ('reading', 'Reading'),
            ('mixed', 'Mixed')
        ],
        default='mixed'
    )
    focus_areas = serializers.ListField(child=serializers.CharField(), required=False, default=list)


class SkillGapAnalysisSerializer(serializers.Serializer):
    target_career_path_id = serializers.IntegerField()
    current_skills_assessment = serializers.DictField(child=serializers.CharField())