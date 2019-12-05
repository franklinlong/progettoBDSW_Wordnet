domain_map = {
    'doctrines': None,
    'archaeology': 'doctrines',
    'astrology': 'doctrines',
    'history': 'doctrines',
    'linguistics': 'doctrines',
    'literature': 'doctrines',
    'philosophy': 'doctrines',
    'psychology': 'doctrines',
    'art': 'doctrines',
    'religion': 'doctrines',

    'factotum': None,
    'number': None,
    'color': None,
    'time_period': None,
    'person': None,
    'quality': None,
    'metrology': None,

    'dance': 'art',
    'drawing': 'art',
    'music': 'art',
    'photography': 'art',
    'plastic_arts': 'art',
    'theatre': 'art',

    'painting': 'drawing',
    'philately': 'drawing',

    'heraldry': 'history',
    'grammar': 'linguistics',

    'philology': 'literature',

    'jewellery': 'plastic_arts',
    'numismatics': 'plastic_arts',
    'sculpture': 'plastic_arts',

    'psychoanalysis': 'psychology',
    'mythology': 'religion',
    'occultism': 'religion',
    'theology': 'religion',

    'free_time': None,
    'play': 'free_time',
    'sport': 'free_time',

    'betting': 'play',
    'card': 'play',
    'chess': 'play',

    'badminton': 'sport',
    'baseball': 'sport',
    'basketball': 'sport',
    'cricket': 'sport',
    'football': 'sport',
    'golf': 'sport',
    'rugby': 'sport',
    'soccer': 'sport',
    'table_tennis': 'sport',
    'tennis': 'sport',
    'volleyball': 'sport',
    'cycling': 'sport',
    'skating': 'sport',
    'skiing': 'sport',
    'hockey': 'sport',
    'mountaineering': 'sport',
    'rowing': 'sport',
    'swimming': 'sport',
    'sub': 'sport',
    'diving': 'sport',
    'racing': 'sport',
    'athletics': 'sport',
    'wrestling': 'sport',
    'boxing': 'sport',
    'fencing': 'sport',
    'archery': 'sport',
    'fishing': 'sport',
    'hunting': 'sport',
    'bowling': 'sport',

    'applied_science': None,
    'agriculture': 'applied_science',
    'alimentation': 'applied_science',
    'architecture': 'applied_science',
    'computer_science': 'applied_science',
    'engineering': 'applied_science',
    'medicine': 'applied_science',
    'veterinary': 'applied_science',

    'gastronomy': 'alimentation',

    'town_planning': 'architecture',
    'building_industry': 'architecture',
    'furniture': 'architecture',

    'mechanics': 'engineering',
    'astronautics': 'engineering',
    'electrotechnics': 'engineering',
    'hydraulics': 'engineering',

    'dentistry': 'medicine',
    'pharmacy': 'medicine',
    'radiology': 'medicine',
    'psychiatry': 'medicine',
    'surgery': 'medicine',

    'zootechnics': 'veterinary',

    'pure_science': None,
    'astronomy': 'pure_science',
    'biology': 'pure_science',
    'chemistry': 'pure_science',
    'earth': 'pure_science',
    'mathematics': 'pure_science',
    'physics': 'pure_science',

    'topography': 'astronomy',

    'biochemistry': 'biology',
    'ecology': 'biology',
    'botany': 'biology',
    'zoology': 'biology',
    'anatomy': 'biology',
    'physiology': 'biology',
    'genetics': 'biology',

    'geology': 'earth',
    'meteorology': 'earth',
    'oceanography': 'earth',
    'paleontology': 'earth',
    'geography': 'earth',

    'geometry': 'mathematics',

    'acoustics': 'physics',
    'atomic_physic': 'physics',
    'electricity': 'physics',
    'optics': 'physics',

    'entomology': 'zoology',

    'social_science': None,
    'administration': 'social_science',
    'anthropology': 'social_science',
    'artisanship': 'social_science',
    'body_care': 'social_science',
    'commerce': 'social_science',
    'economy': 'social_science',
    'fashion': 'social_science',
    'industry': 'social_science',
    'law': 'social_science',
    'military': 'social_science',
    'pedagogy': 'social_science',
    'politics': 'social_science',
    'publishing': 'social_science',
    'sexuality': 'social_science',
    'sociology': 'social_science',
    'telecommunication': 'social_science',
    'tourism': 'social_science',
    'transport': 'social_science',

    'ethnology': 'anthropology',

    'folklore': 'ethnology',

    'banking': 'economy',
    'book_keeping': 'economy',
    'enterprise': 'economy',
    'exchange': 'economy',
    'insurance': 'economy',
    'money': 'economy',
    'tax': 'economy',

    'state': 'law',

    'school': 'pedagogy',
    'university': 'pedagogy',

    'diplomacy': 'politics',

    'cinema': 'telecommunication',
    'post': 'telecommunication',
    'radio': 'telecommunication',
    'telegraphy': 'telecommunication',
    'telephony': 'telecommunication',
    'tv': 'telecommunication',

    'aeronautic': 'transport',
    'auto': 'transport',
    'merchant_navy': 'transport',
    'railway': 'transport',
}


def lista_domini_padre (dom_partenza):
    lista = [dom_partenza]
    try:
        while domain_map[dom_partenza] is not None:
            lista.append(domain_map[dom_partenza])
            dom_partenza = domain_map[dom_partenza]
    except:
        lista = [dom_partenza]

    return lista


