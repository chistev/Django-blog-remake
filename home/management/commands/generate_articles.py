import random
from django.utils import timezone
from django.core.management.base import BaseCommand

from home.models import Article, Category

class Command(BaseCommand): # MUST be named "Command"
    help = 'Generate sample articles for testing'

    def add_arguments(self, parser): # Defines command-line arguments
        parser.add_argument(
            '--count',
            type=int,
            default=23,
            help='Number of articles to create (default:23)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing articles before generating new ones'
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']

        if clear:
            Article.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all existing articles'))
        
        categories_data = [
            'Technology', 'Science', 'Health', 'Business', 
            'Politics', 'Sports', 'Entertainment', 'Travel',
            'Food', 'Education', 'Environment', 'Culture'
        ]
        
        # categories = [<Category: Technology>, <Category: Science>, <Category: Health>]
        # LIST OF CATEGORY OBJECTS
        categories = []  
        for category_name in categories_data:
            category, created = Category.objects.get_or_create(
                # One lookup field, defaults for everything else
                name=category_name,
                defaults={
                    'slug':category_name.lower()
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category_name}')
                
        sample_titles = [
            "The Future of Artificial Intelligence in Everyday Life",
            "Breakthrough Discovery in Quantum Computing",
            "Climate Change: Urgent Actions Needed Now",
            "The Rise of Remote Work and Digital Nomads",
            "Mental Health Awareness in the Modern Workplace",
            "Sustainable Energy Solutions for Tomorrow",
            "The Evolution of Social Media Platforms",
            "Cryptocurrency: The Future of Digital Finance",
            "Innovations in Medical Technology",
            "The Art of Mindful Living in a Busy World",
            "Space Exploration: New Frontiers Await",
            "The Impact of 5G Technology on Society",
            "Plant-Based Diets: Health and Environmental Benefits",
            "The Psychology of Decision Making",
            "Artificial Intelligence in Healthcare",
            "The Future of Electric Vehicles",
            "Cybersecurity Threats in the Digital Age",
            "The Power of Positive Thinking",
            "Blockchain Technology Beyond Cryptocurrency",
            "The Rise of E-commerce and Online Shopping",
            "Education in the Digital Era",
            "The Importance of Work-Life Balance",
            "Smart Cities: Urban Planning for the Future"
        ]
        
        sample_contents = [
            "In recent years, this topic has gained significant attention from experts worldwide. Research shows that innovative approaches are transforming how we think about this subject. This article explores the latest developments and their implications for the future.",
            
            "The rapid advancement in this field has led to unprecedented opportunities. Scientists and researchers are working tirelessly to unlock new possibilities. This comprehensive analysis covers the key trends and breakthroughs shaping our understanding.",
            
            "As we navigate the complexities of modern life, this issue has become increasingly relevant. From economic impacts to social changes, the effects are far-reaching. This piece examines the various perspectives and offers insights into potential solutions.",
            
            "Understanding this phenomenon requires a deep dive into its historical context and current manifestations. The evidence suggests that we are at a turning point. This article presents a thorough examination of the challenges and opportunities ahead.",
            
            "Experts agree that this area will continue to evolve rapidly in the coming years. The convergence of technology, policy, and human behavior creates both opportunities and challenges. This analysis provides a comprehensive overview of the current landscape.",
            
            "The implications of this development are profound and long-lasting. As we adapt to changing circumstances, new paradigms are emerging. This article explores the transformative potential and what it means for various stakeholders.",
            
            "Recent studies have shed new light on this topic, challenging conventional wisdom. The data reveals surprising patterns and trends that demand our attention. This piece offers a detailed exploration of the findings and their significance.",
            
            "Innovation in this space is accelerating at an unprecedented pace. From startups to established companies, everyone is racing to adapt. This article examines the key players, technologies, and trends driving this transformation.",
            
            "The intersection of technology and human experience is creating fascinating new possibilities. This article delves into the ways these developments are reshaping our world and what the future might hold.",
            
            "Understanding the complexities of this subject requires careful analysis and open-mindedness. This comprehensive guide provides readers with the knowledge and insights needed to navigate this evolving landscape."
        ]
        
        created_count = 0
        used_titles = {}
        
        for i in range(count):
            base_title = random.choice(sample_titles)
            
            if base_title in used_titles:
                used_titles[base_title] += 1
                title = f'{base_title} Part {used_titles[base_title]}'
            else:
                used_titles[base_title] = 1
                title = base_title
                
            content = random.choice(sample_contents)
            
            paragraphs = [
                "This detailed analysis provides a comprehensive overview of the current state of affairs.",
                "Several key factors contribute to the complexity of this issue, requiring a nuanced understanding.",
                "The implications of these developments extend far beyond initial expectations.",
                "Experts are cautiously optimistic about the future prospects in this area.",
                "This article synthesizes research from leading authorities in the field.",
                "The evidence presented here challenges many commonly held assumptions.",
                "Looking ahead, several emerging trends promise to reshape our understanding.",
                "The collaborative efforts of researchers worldwide have yielded remarkable insights."
            ]
            
            extra_paragraphs = random.sample(paragraphs, k=random.randint(0,3))
            full_content = content + "\n\n" +"\n\n".join(extra_paragraphs) 
            
            days_ago = random.randint(0, 60)
            published_date = timezone.now() - timezone.timedelta(days=days_ago)
            
            is_published = random.random() > 0.1
            
            article = Article.objects.create(
                title=title,
                content=full_content,
                category=random.choice(categories),
                published_date=published_date,
                is_published=is_published,
                image_url=random.choice([
                    'https://images.pexels.com/photos/572056/pexels-photo-572056.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                    'https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                    'https://images.pexels.com/photos/220201/pexels-photo-220201.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                    'https://images.pexels.com/photos/256417/pexels-photo-256417.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                    'https://images.pexels.com/photos/2662116/pexels-photo-2662116.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
                    '',
                    '',
                    '',
                    '',
                ]),
                )
            
            created_count += 1
            if created_count % 5 == 0:
                self.stdout.write(f'Created {created_count} articles')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} articles'))
        
        published_count = Article.objects.filter(is_published=True).count()
        unpublished_count = Article.objects.filter(is_published=False).count()
        category_count = Category.objects.count()
        
        self.stdout.write(f'Statistics:')
        self.stdout.write(f'  - Published articles: {published_count}')
        self.stdout.write(f'  - Unpublished articles: {unpublished_count}')
        self.stdout.write(f'  - Total categories: {category_count}')
            