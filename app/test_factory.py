from io import BytesIO

from PIL import Image
from django_dynamic_fixture import G

from django.core.files.uploadedfile import InMemoryUploadedFile


from cms.models import Page
from common.models import FixedBlock
from product.models import Equipment
from product.models import EquipmentCategory
from product.models import EquipmentSubCategory
from product.models import EquipmentIndustry
from product.models import EquipmentSubIndustry


def get_test_image():
    """Returns an image for running tests
    """
    io = BytesIO()
    size = (10, 10)
    color = (255, 0, 0, 0)

    image = Image.new('RGBA', size, color)
    image.save(io, format='PNG')
    image_file = InMemoryUploadedFile(
        io, None, 'test.jpg', 'jpeg', image.size, None
    )
    image_file.seek(0)

    return image_file


class DataFactory:
    category = None
    equipment = None
    fixed_block = None
    sub_category = None

    def __init__(self):
        self.fixed_block = FixedBlock.objects.create(
            image=get_test_image(),
            title="new_equipment",
            slug="new_equipment",
            summary="summary",
        )

        G(FixedBlock, slug='industry_equipment')
        G(FixedBlock, slug='used_equipment')
        G(FixedBlock, slug='rental_equipment')
        G(FixedBlock, slug='allied_equipment')

        G(Page, slug='nosotros')
        G(Page, slug='tecnologia')
        G(Page, slug='financiacion')
        G(Page, slug='renta')
        G(Page, slug='legal')
        G(Page, slug='industrias')
        G(Page, slug='repuestos-y-servicios')

        self.equipment_sub_category = G(
            EquipmentSubCategory,
            is_active=True,
            video_url='https://www.youtube.com/watch?v=697EbMJei_Q',
        )

        self.equipment = G(
            Equipment,
            for_rental=True,
        )

        self.equipment.subcategories.add(self.equipment_sub_category)

        self.equipment_category = G(
            EquipmentCategory,
            is_active=True,
        )

        self.equipment_category.subcategories.add(self.equipment_sub_category)

        self.equipment_industry = G(
            EquipmentIndustry,
            is_active=True,
        )

        self.equipment_sub_industry = G(
            EquipmentSubIndustry,
            industry=self.equipment_industry,
            is_active=True,
        )

        self.equipment.subindustries.add(self.equipment_sub_industry)
