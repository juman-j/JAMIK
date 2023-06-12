# import json
# from fastapi import APIRouter, Depends
# from sqlalchemy import column, func, insert, select, table
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.database import get_async_session
# from src.models.models import allergen


# router = APIRouter()

# @router.on_event("startup")
# async def startup():
#     await create_initial_data()


# async def has_existing_data(session):
#     my_table = table("allergen", column("allergen_id"))
#     stmt = select(func.count()).select_from(my_table)

#     count = await (await session.execute(stmt)).scalar()

#     print(count)
#     return count > 0


# async def create_initial_data():
#   async for session in get_async_session():
#     if await has_existing_data(session):   
#       insert_statement = insert(allergen).values(
#         [
#             {
#                 "allergen_id": "1a",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "obiloviny - podskupina: 1a - obilovina obsahující lepek - pšenice",
#                         "EN": "cereals - subgroup: 1a - gluten-containing cereal - wheat",
#                         "DE": "Getreide - Untergruppe: 1a - glutenhaltiges Getreide - Weizen",
#                         "ES": "cereales - subgrupo: 1a - cereal que contiene gluten - trigo",
#                         "FR": "céréales - sous-groupe: 1a - céréale contenant du gluten - blé",
#                         "UK": "злаки - підгрупа: 1a - злаки, що містять глютен - пшениця",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "1b",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "obilovina obsahující lepek - žito",
#                         "EN": "gluten-containing cereal - rye",
#                         "DE": "glutenhaltiges Getreide - Roggen",
#                         "ES": "cereal que contiene gluten - centeno",
#                         "FR": "céréale contenant du gluten - seigle",
#                         "UK": "злаки, що містять глютен - жито",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "1c",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "obilovina obsahující lepek - ječmen",
#                         "EN": "gluten-containing cereal - barley",
#                         "DE": "glutenhaltiges Getreide - Gerste",
#                         "ES": "cereal que contiene gluten - cebada",
#                         "FR": "céréale contenant du gluten - orge",
#                         "UK": "злаки, що містять глютен - ячмінь",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "1d",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "obilovina obsahující lepek - oves",
#                         "EN": "gluten-containing cereal - oats",
#                         "DE": "glutenhaltiges Getreide - Hafer",
#                         "ES": "cereal que contiene gluten - avena",
#                         "FR": "céréale contenant du gluten - avoine",
#                         "UK": "злаки, що містять глютен - вівса",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "1e",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "obilovina obsahující lepek - špalda",
#                         "EN": "gluten-containing cereal - spelt",
#                         "DE": "glutenhaltiges Getreide - Dinkel",
#                         "ES": "cereal que contiene gluten - espelta",
#                         "FR": "céréale contenant du gluten - épeautre",
#                         "UK": "злаки, що містять глютен - спельта",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "1f",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "obilovina obsahující lepek - kamut",
#                         "EN": "gluten-containing cereal - kamut",
#                         "DE": "glutenhaltiges Getreide - Kamut",
#                         "ES": "cereal que contiene gluten - kamut",
#                         "FR": "céréale contenant du gluten - kamut",
#                         "UK": "злаки, що містять глютен - камут",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "02",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "korýši a výrobky z nich",
#                         "EN": "crustaceans and products thereof",
#                         "DE": "Krebstiere und daraus gewonnene Erzeugnisse",
#                         "ES": "crustáceos y productos a base de crustáceos",
#                         "FR": "crustacés et produits à base de crustacés",
#                         "UK": "ракоподібні та продукти з них",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "03",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "vejce a výrobky z nich",
#                         "EN": "eggs and products thereof",
#                         "DE": "Eier und daraus gewonnene Erzeugnisse",
#                         "ES": "huevos y productos a base de huevos",
#                         "FR": "œufs et produits à base d’œufs",
#                         "UK": "яйця та продукти з них",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "04",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "ryby a výrobky z nich",
#                         "EN": "fish and products thereof",
#                         "DE": "Fisch und daraus gewonnene Erzeugnisse",
#                         "ES": "pescado y productos a base de pescado",
#                         "FR": "poissons et produits à base de poissons",
#                         "UK": "риба та продукти з риби",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "05",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "jádra a výrobky z nich",
#                         "EN": "peanuts and products thereof",
#                         "DE": "Erdnüsse und daraus gewonnene Erzeugnisse",
#                         "ES": "cacahuetes y productos a base de cacahuetes",
#                         "FR": "arachides et produits à base d’arachides",
#                         "UK": "арахіс та продукти з арахісу",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "06",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "sójové boby a výrobky z nich",
#                         "EN": "soybeans and products thereof",
#                         "DE": "Sojabohnen und daraus gewonnene Erzeugnisse",
#                         "ES": "soja y productos a base de soja",
#                         "FR": "soja et produits à base de soja",
#                         "UK": "соя та продукти з сої",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "07",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "mléko a výrobky z něj",
#                         "EN": "milk and products thereof",
#                         "DE": "Milch und daraus gewonnene Erzeugnisse",
#                         "ES": "leche y productos a base de leche",
#                         "FR": "lait et produits à base de lait",
#                         "UK": "молоко та продукти з нього",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8a",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8a - skořáp. plody a výrobky z nich - mandle",
#                         "EN": "tree nuts - subgroup: 8a - tree nuts and products thereof - almonds",
#                         "DE": "Schalenfrüchte - Untergruppe: 8a - Schalenfrüchte und daraus gewonnene Erzeugnisse - Mandeln",
#                         "ES": "frutos secos - subgrupo: 8a - frutos secos y productos a base de ellos - almendras",
#                         "FR": "fruits à coque - sous-groupe: 8a - fruits à coque et produits à base de ces fruits - amandes",
#                         "UK": "горіхи - підгрупа: 8a - горіхи та продукти з них - мигдаль",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8b",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8b - skořáp. plody a výrobky z nich - lístkové ořechy",
#                         "EN": "tree nuts - subgroup: 8b - tree nuts and products thereof - hazelnuts",
#                         "DE": "Schalenfrüchte - Untergruppe: 8b - Schalenfrüchte und daraus gewonnene Erzeugnisse - Haselnüsse",
#                         "ES": "frutos secos - subgrupo: 8b - frutos secos y productos a base de ellos - avellanas",
#                         "FR": "fruits à coque - sous-groupe: 8b - fruits à coque et produits à base de ces fruits - noisettes",
#                         "UK": "горіхи - підгрупа: 8b - горіхи та продукти з них - лісові горіхи",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8c",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8c - skořáp. plody a výrobky z nich - vlašské ořechy",
#                         "EN": "tree nuts - subgroup: 8c - tree nuts and products thereof - walnuts",
#                         "DE": "Schalenfrüchte - Untergruppe: 8c - Schalenfrüchte und daraus gewonnene Erzeugnisse - Walnüsse",
#                         "ES": "frutos secos - subgrupo: 8c - frutos secos y productos a base de ellos - nueces",
#                         "FR": "fruits à coque - sous-groupe: 8c - fruits à coque et produits à base de ces fruits - noix",
#                         "UK": "горіхи - підгрупа: 8c - горіхи та продукти з них - горіхи",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8d",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8d - skořáp. plody a výrobky z nich - kešu",
#                         "EN": "tree nuts - subgroup: 8d - tree nuts and products thereof - cashews",
#                         "DE": "Schalenfrüchte - Untergruppe: 8d - Schalenfrüchte und daraus gewonnene Erzeugnisse - Cashewnüsse",
#                         "ES": "frutos secos - subgrupo: 8d - frutos secos y productos a base de ellos - anacardos",
#                         "FR": "fruits à coque - sous-groupe: 8d - fruits à coque et produits à base de ces fruits - noix de cajou",
#                         "UK": "горіхи - підгрупа: 8d - горіхи та продукти з них - кеш",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8e",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8e - skořáp. plody a výrobky z nich - para ořechy",
#                         "EN": "tree nuts - subgroup: 8e - tree nuts and products thereof - pecans",
#                         "DE": "Schalenfrüchte - Untergruppe: 8e - Schalenfrüchte und daraus gewonnene Erzeugnisse - Pekannüsse",
#                         "ES": "frutos secos - subgrupo: 8e - frutos secos y productos a base de ellos - nueces pecanas",
#                         "FR": "fruits à coque - sous-groupe: 8e - fruits à coque et produits à base de ces fruits - noix de pécan",
#                         "UK": "горіхи - підгрупа: 8e - горіхи та продукти з них - пекан",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8f",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8f - skořáp. plody a výrobky z nich - pistácie",
#                         "EN": "tree nuts - subgroup: 8f - tree nuts and products thereof - pistachios",
#                         "DE": "Schalenfrüchte - Untergruppe: 8f - Schalenfrüchte und daraus gewonnene Erzeugnisse - Pistazien",
#                         "ES": "frutos secos - subgrupo: 8f - frutos secos y productos a base de ellos - pistachos",
#                         "FR": "fruits à coque - sous-groupe: 8f - fruits à coque et produits à base de ces fruits - pistaches",
#                         "UK": "горіхи - підгрупа: 8f - горіхи та продукти з них - фісташки",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "8g",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "skořápkové plody - podskupina: 8g - skořáp. plody a výrobky z nich - makadamie",
#                         "EN": "tree nuts - subgroup: 8g - tree nuts and products thereof - macadamia nuts",
#                         "DE": "Schalenfrüchte - Untergruppe: 8g - Schalenfrüchte und daraus gewonnene Erzeugnisse - Macadamianüsse",
#                         "ES": "frutos secos - subgrupo: 8g - frutos secos y productos a base de ellos - nueces de macadamia",
#                         "FR": "fruits à coque - sous-groupe: 8g - fruits à coque et produits à base de ces fruits - noix de macadamia",
#                         "UK": "горіхи - підгрупа: 8g - горіхи та продукти з них - макадамія",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "09",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "celer a výrobky z něj",
#                         "EN": "celery and products thereof",
#                         "DE": "Sellerie und daraus gewonnene Erzeugnisse",
#                         "ES": "apio y productos a base de apio",
#                         "FR": "céleri et produits dérivés",
#                         "UK": "селера та продукти з нього",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "10",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "hořčice a výrobky z ní",
#                         "EN": "mustard and products thereof",
#                         "DE": "Senf und daraus gewonnene Erzeugnisse",
#                         "ES": "mostaza y productos a base de mostaza",
#                         "FR": "moutarde et produits à base de moutarde",
#                         "UK": "гірчиця та продукти з неї",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "11",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "sezamová semena a výrobky z nich",
#                         "EN": "sesame seeds and products thereof",
#                         "DE": "Sesamsamen und daraus gewonnene Erzeugnisse",
#                         "ES": "semillas de sésamo y productos a base de ellas",
#                         "FR": "graines de sésame et produits à base de ces graines",
#                         "UK": "кунжут та продукти з нього",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "12",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "oxid siřičitý a siřičitany",
#                         "EN": "sulfur dioxide and sulfites",
#                         "DE": "Schwefeldioxid und Sulfite",
#                         "ES": "dióxido de azufre y sulfitos",
#                         "FR": "dioxyde de soufre et sulfites",
#                         "UK": "діоксид сірки та сульфіти",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "13",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "vlčí bob a výrobky z něj",
#                         "EN": "lupin and products thereof",
#                         "DE": "Lupine und daraus gewonnene Erzeugnisse",
#                         "ES": "altramuces y productos a base de altramuces",
#                         "FR": "lupin et produits à base de lupin",
#                         "UK": "люпин та продукти з нього",
#                     }
#                 ),
#             },
#             {
#                 "allergen_id": "14",
#                 "allergen_name": json.dumps(
#                     {
#                         "CS": "měkkýši a výrobky z nich",
#                         "EN": "molluscs and products thereof",
#                         "DE": "Weichtiere und daraus gewonnene Erzeugnisse",
#                         "ES": "moluscos y productos a base de moluscos",
#                         "FR": "mollusques et produits à base de mollusques",
#                         "UK": "молюски та продукти з них",
#                     }
#                 ),
#             },
#         ]
#       )
#       await session.execute(insert_statement)
#       await session.commit()
