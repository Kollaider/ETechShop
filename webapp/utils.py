
def generate_networknode_contact_info(network_node):

    network_node_data = {}

    contact_obj = network_node.contact
    email = contact_obj.email

    address_obj = contact_obj.address
    network_node_data['country'] = address_obj.country
    network_node_data['city'] = address_obj.city
    network_node_data['street'] = address_obj.street
    network_node_data['house_number'] = address_obj.house_number

    return email, network_node_data
