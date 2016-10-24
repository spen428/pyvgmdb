import logging
import pyvgmdb.pyvgmdb


class VGMdbObject(object):
    def __init__(self, data):
        # Add json data to the attribute dictionary
        for key in data:
            setattr(self, key, data[key])
        # All results (should) have a "link" field
        # Parse `link`, which should be of the form "category/12345", to get the id
        try:
            val = int(self.link.split("/")[-1])
        except (TypeError, ValueError):
            # Parse failed, worry about it later
            val = None
            logging.warning("Could not determine id of VGMdbObject with link '{}'"
                            .format(self.link))
        self.id = val

    def __str__(self):
        return "{}:{}".format(type(self).__name__, self.__dict__.__str__())

    def __repr__(self):
        return "{}:{}".format(type(self).__name__, self.__dict__.__repr__())


class VGMdbAlbumSummary(VGMdbObject):
    def get_album(self):
        """Get the full details of this album
        :return: A VGMdbAlbum object
        """
        return pyvgmdb.get_album(self.id)


class VGMdbArtistSummary(VGMdbObject):
    def get_artist(self):
        """Get the full details of this artist
        :return: A VGMdbArtist object
        """
        return pyvgmdb.get_artist(self.id)


class VGMdbOrgSummary(VGMdbObject):
    def get_org(self):
        """Get the full details of this org
        :return: A VGMdbOrg object
        """
        return pyvgmdb.get_org(self.id)


class VGMdbProductSummary(VGMdbObject):
    def get_product(self):
        """Get the full details of this product
        :return: A VGMdbProduct object
        """
        return pyvgmdb.get_product(self.id)


class VGMdbAlbum(VGMdbObject):
    def __init__(self, data):
        super(VGMdbAlbum, self).__init__(data)
        # Parse contained products into VGMdbProductSummary objects
        products = [VGMdbProductSummary(e) for e in self.products]
        self.products = products # Overwrite the original entry
        # Same deal for artists
        self.composers = [VGMdbArtistSummary(e) for e in self.composers]
        self.lyricists = [VGMdbArtistSummary(e) for e in self.lyricists]
        self.performers = [VGMdbArtistSummary(e) for e in self.performers]


class VGMdbArtist(VGMdbObject):
    pass


class VGMdbOrg(VGMdbObject):
    def __init__(self, data):
        super(VGMdbOrg, self).__init__(data)
        # Parse contained albums into VGMdbAlbumSummary objects
        self.releases = [VGMdbAlbumSummary(e) for e in self.releases]
        self.albums = self.releases  # Add an alias
        # Same deal for artists
        self.staff = [VGMdbArtistSummary(e) for e in self.staff]
        self.artists = self.staff


class VGMdbProduct(VGMdbObject):
    def __init__(self, data):
        super(VGMdbProduct, self).__init__(data)
        # Parse contained albums into VGMdbAlbumSummary objects
        self.albums = [VGMdbAlbumSummary(e) for e in self.albums]
