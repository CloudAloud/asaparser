import xlsxwriter

def convertSubnetMask(mask):
    """ Converts decimal netmask to bits"""

    newmask = 0

    matrix = {
        '255': 8,
        '254': 7,
        '252': 6,
        '248': 5,
        '240': 4,
        '192': 3,
        '224': 2,
        '128': 1,
        '0': 0
    }

    for octet in mask.split('.'):
        newmask += matrix[octet]

    return newmask

def findObject(object, extLists):
    lists = extLists[:]
    if len(lists) == 0:
        return object
    else:
        currentList = lists.pop(0)
        if currentList.get(object):

            for child in currentList.get(object).children:
                return findObject(child, lists)
        else:
            return findObject(object, lists)


def friteXLSX(filename, input):
    """ This function crates XLSX file from input"""

    # Create and open XLSX file
    workbook = xlsxwriter.Workbook(filename)

    # Create sheet in XLSX file
    worksheet = workbook.add_worksheet('Policy')

    # Initialize position
    row, col = 0, 0

    # Bold font format
    bold = workbook.add_format({'bold': True})

    # Write heading
    worksheet.write(row, col, 'ACL name', bold)
    worksheet.write(row, col + 1, 'Protocol', bold)
    worksheet.write(row, col + 2, 'Source', bold)
    worksheet.write(row, col + 3, 'Destination', bold)
    worksheet.write(row, col + 4, 'Service', bold)
    worksheet.write(row, col + 5, 'Remark', bold)
    row += 1

    # Write results
    for acl, action, protocol, source, destination, service, remark in (input):
        worksheet.write(row, col, acl)
        worksheet.write(row, col + 1, protocol)
        worksheet.write(row, col + 2, source)
        worksheet.write(row, col + 3, destination)
        worksheet.write(row, col + 4, service)
        worksheet.write(row, col + 5, remark)
        row += 1

    # Close XLSX file
    workbook.close()
